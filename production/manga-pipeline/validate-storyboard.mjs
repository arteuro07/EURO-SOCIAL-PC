import fs from 'node:fs';

const file = process.argv[2] || 'episodes/proof-kevin/storyboard.json';
const data = JSON.parse(fs.readFileSync(file, 'utf8'));
const errors = [];
if (data.format !== 'vertical-9:16') errors.push('format must be vertical-9:16');
if (![24, 30].includes(data.fps)) errors.push('fps must be 24 or 30');
if (!(data.duration_seconds > 0 && data.duration_seconds <= 60)) errors.push('duration must be between 0 and 60 seconds');
if (!Array.isArray(data.shots) || data.shots.length === 0) errors.push('at least one shot is required');

let cursor = 0;
const ids = new Set();
for (const [i, shot] of (data.shots || []).entries()) {
  const label = shot.id || `shot[${i}]`;
  if (!shot.id || ids.has(shot.id)) errors.push(`${label}: missing or duplicate id`);
  ids.add(shot.id);
  if (typeof shot.start !== 'number' || typeof shot.end !== 'number' || shot.end <= shot.start) errors.push(`${label}: invalid time range`);
  if (Math.abs(shot.start - cursor) > 0.001) errors.push(`${label}: timeline gap/overlap; expected start ${cursor.toFixed(3)}s`);
  if (Array.isArray(shot.layers) && shot.layers.length === 0) errors.push(`${label}: no visual layers`);
  cursor = shot.end;
}
if (Math.abs(cursor - data.duration_seconds) > 0.001) errors.push(`last shot ends at ${cursor}s, duration is ${data.duration_seconds}s`);

if (errors.length) {
  console.error('STORYBOARD INVALID');
  for (const error of errors) console.error('- ' + error);
  process.exit(1);
}
console.log(`STORYBOARD OK: ${data.episode_id} — ${data.shots.length} shots, ${data.duration_seconds}s at ${data.fps} fps`);
console.log('NOTE: validation checks structure and timing, not visual quality or asset existence.');
