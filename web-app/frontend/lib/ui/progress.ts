export type ProgressResult = {
  progress: number;
  leftPercent: number;
  hasDuration: boolean;
};

export const computeProgress = (start?: string, end?: string, now: Date = new Date()): ProgressResult => {
  if (!start || !end) {
    return { progress: 0, leftPercent: 100, hasDuration: false };
  }
  const s = new Date(start);
  const e = new Date(end);
  if (!(s instanceof Date) || isNaN(s.getTime()) || !(e instanceof Date) || isNaN(e.getTime())) {
    return { progress: 0, leftPercent: 100, hasDuration: false };
  }
  const total = Math.max(0, e.getTime() - s.getTime());
  if (total === 0) {
    return { progress: 1, leftPercent: 0, hasDuration: true };
  }
  const elapsed = Math.max(0, now.getTime() - s.getTime());
  const prog = Math.min(1, Math.max(0, elapsed / total));
  const left = Math.round((1 - prog) * 100);
  return { progress: prog, leftPercent: left, hasDuration: true };
};

export const runProgressTests = () => {
  const now = new Date('2025-01-01T00:00:00Z');
  const results: Array<{ name: string; pass: boolean }> = [];
  const add = (name: string, pass: boolean) => results.push({ name, pass });
  const r1 = computeProgress(undefined, undefined, now);
  add('empty duration', r1.progress === 0 && r1.leftPercent === 100 && r1.hasDuration === false);
  const r2 = computeProgress('2025-01-01T00:00:00Z', '2025-01-01T00:00:00Z', now);
  add('zero duration', r2.progress === 1 && r2.leftPercent === 0 && r2.hasDuration === true);
  const r3 = computeProgress('2024-01-01T00:00:00Z', '2026-01-01T00:00:00Z', new Date('2024-01-01T00:00:00Z'));
  add('0% complete', r3.progress === 0 && r3.leftPercent === 100);
  const r4 = computeProgress('2024-01-01T00:00:00Z', '2026-01-01T00:00:00Z', new Date('2026-01-01T00:00:00Z'));
  add('100% complete', r4.progress === 1 && r4.leftPercent === 0);
  return results;
};