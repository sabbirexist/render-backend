from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def home():
    return 'YTDLP API is running!'

@app.route('/api/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get('url')
    media_type = data.get('type')  # 'video' or 'audio'

    if not url or media_type not in ['video', 'audio']:
        return jsonify({'error': 'Invalid request'}), 400

    output_file = '/tmp/media.%(ext)s'
    ytdlp_cmd = [
        'yt-dlp',
        url,
        '-o', output_file,
        '--no-skip-download',
        '--no-check-certificates',
        '--prefer-free-formats',
        '--no-warnings',
        '--no-embed-thumbnail',
        '--no-verbose',
    ]

    if media_type == 'video':
        ytdlp_cmd += ['--format', 'bestvideo+bestaudio/best']
    elif media_type == 'audio':
        ytdlp_cmd += ['--extract-audio', '--audio-format', 'mp3']

    try:
        result = subprocess.run(ytdlp_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            return jsonify({'error': result.stderr}), 500
        return jsonify({'message': 'Downloaded successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
