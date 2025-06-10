from flask import Flask, request, jsonify, send_file
import subprocess
import os
import uuid

app = Flask(__name__)

@app.route('/api/download', methods=['POST'])
def download():
    data = request.json
    url = data.get('url')
    media_type = data.get('type', 'video')  # 'video' or 'audio'

    if not url:
        return jsonify({'error': 'URL is required'}), 400

    temp_id = str(uuid.uuid4())
    output_template = f"/tmp/{temp_id}.%(ext)s"

    # yt-dlp command
    cmd = [
        "yt-dlp",
        url,
        "-o", output_template,
    ]

    if media_type == "audio":
        cmd += ["--extract-audio", "--audio-format", "mp3"]

    try:
        subprocess.run(cmd, check=True)
        # Find the actual file
        output_files = [f for f in os.listdir("/tmp") if temp_id in f]
        if not output_files:
            return jsonify({"error": "Download failed"}), 500
        filepath = os.path.join("/tmp", output_files[0])
        return send_file(filepath, as_attachment=True)
    except subprocess.CalledProcessError as e:
        return jsonify({"error": "yt-dlp failed", "details": str(e)}), 500

@app.route('/')
def home():
    return 'Backend is running!'
