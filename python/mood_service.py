from flask import Flask, request, jsonify
import os

from mood_analysis import analyze_mood

app = Flask(__name__)


@app.get("/mood")
def mood():
    file = request.args.get("file")
    if not file or not os.path.isfile(file):
        return jsonify({"error": "Missing or invalid file parameter"}), 400
    try:
        return jsonify(analyze_mood(file))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # The built-in Flask server is for local development only.
    # For production, run with a WSGI server such as:
    #   gunicorn -b 0.0.0.0:5000 mood_service:app
    app.run(host="0.0.0.0", port=5000)
