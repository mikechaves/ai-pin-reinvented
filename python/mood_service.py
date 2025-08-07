from flask import Flask, request, jsonify
import os

from mood_analysis import analyze_mood

app = Flask(__name__)


@app.get("/mood")
def mood():
    file_path = request.args.get("file")
    if not file_path:
        return jsonify({"error": "Missing file parameter"}), 400

    # Security: ensure file is within project directory and is a file
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    abs_path = os.path.abspath(file_path)

    if not abs_path.startswith(project_root) or not os.path.isfile(abs_path):
        return jsonify({"error": "File is invalid or outside allowed directory"}), 400

    try:
        return jsonify(analyze_mood(abs_path))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # The built-in Flask server is for local development only.
    # For production, run with a WSGI server such as:
    #   gunicorn -b 0.0.0.0:5000 mood_service:app
    app.run(host="0.0.0.0", port=5000)
