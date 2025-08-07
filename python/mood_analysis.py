import sys
import os
import json
import numpy as np
import librosa
import whisper

HIGH_WPM_THRESHOLD = 160
MEDIUM_WPM_THRESHOLD = 120
HIGH_RMS_THRESHOLD = 0.05
MEDIUM_RMS_THRESHOLD = 0.03

SUGGESTIONS = {
    "low": "You're sounding relaxed. Keep it up!",
    "medium": "Take a deep breath and slow down a bit.",
    "high": "Pause and breathe deeply to calm yourself.",
}


model = whisper.load_model("tiny")


def analyze_mood(audio_path: str) -> dict:
    audio, sr = librosa.load(audio_path, sr=None)
    duration_minutes = len(audio) / sr / 60.0 if sr else 0
    rms = float(np.sqrt(np.mean(audio ** 2))) if len(audio) else 0

    result = model.transcribe(audio_path)
    text = result.get("text", "").strip()
    words = len(text.split()) if text else 0
    wpm = words / duration_minutes if duration_minutes > 0 else 0

    if wpm > HIGH_WPM_THRESHOLD or rms > HIGH_RMS_THRESHOLD:
        level = "high"
    elif wpm > MEDIUM_WPM_THRESHOLD or rms > MEDIUM_RMS_THRESHOLD:
        level = "medium"
    else:
        level = "low"

    return {"stress_level": level, "suggestion": SUGGESTIONS[level]}


def main():
    if len(sys.argv) < 2:
        print("Missing file path", file=sys.stderr)
        sys.exit(1)

    audio_path = sys.argv[1]
    if not os.path.isfile(audio_path):
        print("File not found", file=sys.stderr)
        sys.exit(1)

    try:
        print(json.dumps(analyze_mood(audio_path)))
    except Exception as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
