import React from 'react';
import { cn } from '@/lib/utils';
import { computeProgress } from '@/lib/ui/progress';

interface ProgressBarProps {
  start?: string;
  end?: string;
  className?: string;
  size?: 'sm' | 'md';
  ariaLabel?: string;
}

export default function ProgressBar({ start, end, className, size = 'md', ariaLabel = 'Period progress' }: ProgressBarProps) {
  const { progress, leftPercent, hasDuration } = computeProgress(start, end);
  const widthClass = size === 'sm' ? 'w-16 sm:w-24 md:w-32' : 'w-32 sm:w-48 md:w-64';

  if (!hasDuration) {
    return (
      <div
        className={cn('relative rounded-md bg-muted/60 text-muted-foreground', widthClass, 'h-6 px-2 flex items-center justify-center shadow-inner', className)}
        role="progressbar"
        aria-label={ariaLabel}
        aria-valuemin={0}
        aria-valuemax={100}
        aria-valuetext={'Duration not specified'}
      >
        <span className="text-[10px]">Duration not specified</span>
      </div>
    );
  }

  const percent = Math.round(progress * 100);
  return (
    <div
      className={cn('relative rounded-md bg-muted/60', widthClass, 'h-6 shadow-inner overflow-hidden', className)}
      role="progressbar"
      aria-label={ariaLabel}
      aria-valuemin={0}
      aria-valuemax={100}
      aria-valuenow={leftPercent}
      aria-valuetext={`${leftPercent}% left`}
    >
      <div
        className={cn('absolute left-0 top-0 h-full rounded-md bg-gradient-to-r from-primary to-primary/70')}
        style={{ width: `${percent}%`, transition: 'width 700ms ease-out' }}
      />
      <div className="absolute inset-0 flex items-center justify-end pr-2">
        <span className="text-[10px] font-medium text-foreground/90 drop-shadow-sm">{leftPercent}% left</span>
      </div>
    </div>
  );
}
