'use client';

import React, { useState, useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import { aiExportApi, AIExportResponse } from '@/lib/api/ai-export';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Loader2, Copy, Check, Sparkles } from 'lucide-react';
import { BirthDetails } from '@/lib/api/charts';

interface AITabProps {
    birthData: BirthDetails;
}

const SECTION_OPTIONS = [
    { id: 'chart', label: 'Charts' },
    { id: 'divisional', label: 'D9' },
    { id: 'panchanga', label: 'Panchanga' },
    { id: 'dasha', label: 'Dasha' },
    { id: 'strength', label: 'Strength' },
    { id: 'yogas', label: 'Yogas' },
    { id: 'doshas', label: 'Doshas' },
    { id: 'transits', label: 'Transits' },
];

const FORMAT_OPTIONS = [
    { id: 'toon', label: 'TOON', desc: 'Most compact (30-60% fewer tokens)' },
    { id: 'markdown', label: 'Markdown', desc: 'Readable' },
    { id: 'json', label: 'JSON', desc: 'Structured' },
];

const PROMPT_TEMPLATES = [
    { id: 'analyze', label: 'Analyze Chart', prompt: 'Analyze this Vedic horoscope and provide comprehensive insights on personality, career, relationships, and life path.' },
    { id: 'predict', label: 'Predict Period', prompt: 'Based on the current dasha periods and transits, what are the major themes and predictions for the next 2 years?' },
    { id: 'career', label: 'Career Focus', prompt: 'Analyze the career prospects, suitable professions, and timing of career changes based on this horoscope.' },
    { id: 'relationship', label: 'Relationships', prompt: 'Analyze the relationship patterns, marriage timing, and compatibility indicators from this horoscope.' },
    { id: 'health', label: 'Health', prompt: 'What health considerations and vulnerabilities should be noted based on this horoscope?' },
    { id: 'remedies', label: 'Remedies', prompt: 'Based on the doshas and weak planets, suggest appropriate Vedic remedies (mantras, gemstones, charity).' },
];

export function AITab({ birthData }: AITabProps) {
    const [format, setFormat] = useState<'toon' | 'markdown' | 'json'>('toon');
    const [sections, setSections] = useState<string[]>(['chart', 'divisional', 'panchanga', 'dasha', 'strength', 'yogas', 'doshas', 'transits']);
    const [copied, setCopied] = useState(false);
    const [selectedPrompt, setSelectedPrompt] = useState<string>('');

    const birthDetailsReady = Boolean(
        birthData.date && birthData.time && birthData.place?.name && typeof birthData.place.latitude === 'number'
    );

    const { data, isLoading, error, refetch } = useQuery({
        queryKey: ['ai-export', birthData.date, birthData.time, birthData.place?.latitude, birthData.place?.longitude, birthData.ayanamsa, format, sections.join(',')],
        queryFn: () => aiExportApi.export({
            birth_details: birthData,
            format,
            sections
        }),
        enabled: birthDetailsReady,
        refetchOnWindowFocus: false,
    });

    const handleToggleSection = (sectionId: string) => {
        setSections(prev =>
            prev.includes(sectionId)
                ? prev.filter(s => s !== sectionId)
                : [...prev, sectionId]
        );
    };

    const handleCopy = async () => {
        if (!data?.output) return;

        let textToCopy = data.output;
        if (selectedPrompt) {
            const template = PROMPT_TEMPLATES.find(p => p.id === selectedPrompt);
            if (template) {
                textToCopy = `${template.prompt}\n\n${data.output}`;
            }
        }

        try {
            await navigator.clipboard.writeText(textToCopy);
            setCopied(true);
            setTimeout(() => setCopied(false), 2000);
        } catch (err) {
            console.error('Failed to copy:', err);
        }
    };

    if (!birthDetailsReady) {
        return (
            <div className="flex items-center justify-center h-full text-sm text-black/50 dark:text-white/50 p-4 text-center">
                <div className="flex flex-col items-center gap-2">
                    <Sparkles className="w-8 h-8 opacity-30" />
                    <span>Enter birth details to generate AI-ready horoscope data</span>
                </div>
            </div>
        );
    }

    return (
        <div className="h-full flex flex-col overflow-hidden">
            <div className="flex-1 overflow-y-auto p-3 space-y-3">

                {/* Controls */}
                <Card className="border border-black/20 dark:border-white/20 bg-white dark:bg-black">
                    <CardContent className="p-3">
                        <div className="flex flex-wrap items-start gap-4">

                            {/* Format Selector */}
                            <div className="flex flex-col gap-1">
                                <span className="text-xs font-semibold text-black/70 dark:text-white/70 uppercase tracking-wide">Format</span>
                                <div className="flex gap-1">
                                    {FORMAT_OPTIONS.map(opt => (
                                        <button
                                            key={opt.id}
                                            onClick={() => setFormat(opt.id as any)}
                                            className={`px-3 py-1.5 text-xs rounded border transition-colors ${format === opt.id
                                                ? 'bg-black text-white dark:bg-white dark:text-black border-black dark:border-white'
                                                : 'bg-white dark:bg-black text-black dark:text-white border-black/20 dark:border-white/20 hover:bg-black/5 dark:hover:bg-white/5'
                                                }`}
                                            title={opt.desc}
                                        >
                                            {opt.label}
                                        </button>
                                    ))}
                                </div>
                            </div>

                            {/* Section Toggles */}
                            <div className="flex flex-col gap-1">
                                <span className="text-xs font-semibold text-black/70 dark:text-white/70 uppercase tracking-wide">Include</span>
                                <div className="flex flex-wrap gap-1">
                                    {SECTION_OPTIONS.map(opt => (
                                        <label
                                            key={opt.id}
                                            className={`flex items-center gap-1 px-2 py-1 text-xs rounded border cursor-pointer transition-colors ${sections.includes(opt.id)
                                                ? 'bg-black/10 dark:bg-white/10 border-black/30 dark:border-white/30'
                                                : 'bg-white dark:bg-black border-black/10 dark:border-white/10 opacity-50'
                                                }`}
                                        >
                                            <input
                                                type="checkbox"
                                                checked={sections.includes(opt.id)}
                                                onChange={() => handleToggleSection(opt.id)}
                                                className="w-3 h-3"
                                            />
                                            <span>{opt.label}</span>
                                        </label>
                                    ))}
                                </div>
                            </div>

                            {/* Prompt Template */}
                            <div className="flex flex-col gap-1">
                                <span className="text-xs font-semibold text-black/70 dark:text-white/70 uppercase tracking-wide">Prompt</span>
                                <select
                                    value={selectedPrompt}
                                    onChange={(e) => setSelectedPrompt(e.target.value)}
                                    className="h-7 text-xs border border-black/20 dark:border-white/20 bg-white dark:bg-black text-black dark:text-white rounded px-2"
                                >
                                    <option value="">No prompt (data only)</option>
                                    {PROMPT_TEMPLATES.map(t => (
                                        <option key={t.id} value={t.id}>{t.label}</option>
                                    ))}
                                </select>
                            </div>
                        </div>
                    </CardContent>
                </Card>

                {/* Output Area */}
                <Card className="border border-black/20 dark:border-white/20 bg-white dark:bg-black flex-1">
                    <CardHeader className="py-2 px-3 border-b border-black/10 dark:border-white/10 flex flex-row items-center justify-between">
                        <CardTitle className="text-xs font-semibold text-black dark:text-white tracking-wide uppercase flex items-center gap-2">
                            <Sparkles className="w-3 h-3" />
                            AI Export Output
                        </CardTitle>
                        <div className="flex items-center gap-3 text-xs text-black/60 dark:text-white/60">
                            {data && !data.error && (
                                <>
                                    <span>{data.chars} chars</span>
                                    <span>~{data.tokens_est} tokens</span>
                                </>
                            )}
                        </div>
                    </CardHeader>
                    <CardContent className="p-0 relative">
                        {isLoading ? (
                            <div className="flex items-center justify-center p-8">
                                <Loader2 className="w-5 h-5 animate-spin text-black dark:text-white" />
                            </div>
                        ) : error || data?.error ? (
                            <div className="p-4 text-sm text-red-600 dark:text-red-400">
                                Error: {data?.error || (error as Error)?.message}
                            </div>
                        ) : (
                            <>
                                {/* Prompt Preview */}
                                {selectedPrompt && (
                                    <div className="p-3 bg-black/5 dark:bg-white/5 border-b border-black/10 dark:border-white/10 text-xs text-black/70 dark:text-white/70 italic">
                                        {PROMPT_TEMPLATES.find(p => p.id === selectedPrompt)?.prompt}
                                    </div>
                                )}

                                {/* Output Textarea */}
                                <textarea
                                    value={data?.output || ''}
                                    readOnly
                                    className="w-full h-64 p-3 text-xs font-mono bg-transparent text-black dark:text-white resize-none focus:outline-none"
                                    placeholder="Output will appear here..."
                                />
                            </>
                        )}
                    </CardContent>
                </Card>

                {/* Copy Button */}
                <div className="flex items-center justify-between">
                    <div className="text-xs text-black/50 dark:text-white/50">
                        Paste this into ChatGPT, Claude, Gemini, or any LLM
                    </div>
                    <button
                        onClick={handleCopy}
                        disabled={!data?.output || isLoading}
                        className={`flex items-center gap-2 px-4 py-2 text-sm font-medium rounded border transition-all ${copied
                            ? 'bg-green-600 text-white border-green-600'
                            : 'bg-black text-white dark:bg-white dark:text-black border-black dark:border-white hover:opacity-80 disabled:opacity-30'
                            }`}
                    >
                        {copied ? (
                            <>
                                <Check className="w-4 h-4" />
                                Copied!
                            </>
                        ) : (
                            <>
                                <Copy className="w-4 h-4" />
                                Copy to Clipboard
                            </>
                        )}
                    </button>
                </div>



            </div>
        </div>
    );
}
