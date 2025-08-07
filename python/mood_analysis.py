import sys
import os
import json
import numpy as np
import librosa
import whisper


def main():
    if len(sys.argv) < 2:
        print("Missing file path", file=sys.stderr)
        sys.exit(1)

    audio_path = sys.argv[1]
    if not os.path.isfile(audio_path):
        print("File not found", file=sys.stderr)
        sys.exit(1)

    try:
        audio, sr = librosa.load(audio_path, sr=None)
        duration_minutes = len(audio) / sr / 60.0 if sr else 0
        rms = float(np.sqrt(np.mean(audio ** 2))) if len(audio) else 0

        model = whisper.load_model("tiny")
        result = model.transcribe(audio_path)
        words = len(result.get("text", "").strip().split())
        wpm = words / duration_minutes if duration_minutes > 0 else 0

        if wpm > 160 or rms > 0.05:
            level = "high"
        elif wpm > 120 or rms > 0.03:
            level = "medium"
        else:
            level = "low"

        suggestions = {
            "low": "You're sounding relaxed. Keep it up!",
            "medium": "Take a deep breath and slow down a bit.",
            "high": "Pause and breathe deeply to calm yourself.",
        }

        print(json.dumps({"stress_level": level, "suggestion": suggestions[level]}))
    except Exception as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
