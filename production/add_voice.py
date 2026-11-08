import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EPISODE = ROOT / 'production' / 'episodes' / 'E001.json'
VIDEO = ROOT / 'dist' / 'BOSS_DE_RIEN_E001.mp4'
ASSETS = ROOT / 'assets' / 'episodes' / 'E001' / 'audio'
VOICES = ROOT / 'assets' / 'voices'
MODELS = {'kevin': 'fr_FR-tom-medium.onnx', 'junior': 'fr_FR-upmc-medium.onnx', 'maya': 'fr_FR-siwis-medium.onnx'}

def main():
    if not VIDEO.is_file():
        raise RuntimeError('La vidéo muette est introuvable.')
    episode = json.loads(EPISODE.read_text(encoding='utf-8'))
    ASSETS.mkdir(parents=True, exist_ok=True)
    tracks = []
    elapsed = 0
    for scene in episode['scenes']:
        lines = scene.get('dialogue', [])
        slot = int(scene['duration_seconds'] * 1000 / max(1, len(lines)))
        for index, line in enumerate(lines):
            character = line['character']
            model = VOICES / MODELS[character]
            if not model.is_file() or not model.with_suffix('.onnx.json').is_file():
                raise RuntimeError('Voix Piper manquante : ' + str(model))
            audio = ASSETS / (scene['id'] + '_' + str(index + 1) + '_' + character + '.wav')
            if not audio.is_file() or audio.stat().st_size < 1000:
                subprocess.run(['piper', '--model', str(model), '--output_file', str(audio)], input=line['text'], text=True, check=True)
            tracks.append((audio, elapsed * 1000 + index * slot))
        elapsed += int(scene['duration_seconds'])
    command = ['ffmpeg', '-y', '-i', str(VIDEO)]
    for audio, delay in tracks:
        command += ['-i', str(audio)]
    filters = []
    labels = []
    for i, (audio, delay) in enumerate(tracks, start=1):
        label = 'v' + str(i)
        filters.append('[' + str(i) + ':a]aresample=48000,adelay=' + str(delay) + '|' + str(delay) + '[' + label + ']')
        labels.append('[' + label + ']')
    filters.append(''.join(labels) + 'amix=inputs=' + str(len(labels)) + ':duration=longest:normalize=0,alimiter=limit=0.95[aout]')
    output = VIDEO.with_name('BOSS_DE_RIEN_E001_VOIX.mp4')
    command += ['-filter_complex', ';'.join(filters), '-map', '0:v', '-map', '[aout]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-t', str(episode['target_duration_seconds']), '-movflags', '+faststart', str(output)]
    subprocess.run(command, check=True)
    print('EPISODE AVEC VOIX : ' + str(output))

if __name__ == '__main__':
    main()