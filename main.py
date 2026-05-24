from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({"status": "EmYtSave API Running"})

@app.route('/info', methods=['GET'])
def get_info():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL required"}), 400
    try:
        ydl_opts = {'quiet': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = []
            for f in info.get('formats', []):
                if f.get('vcodec') != 'none' and f.get('height'):
                    formats.append({
                        "format_id": f['format_id'],
                        "quality": f"{f['height']}p",
                        "ext": f.get('ext'),
                        "filesize": f.get('filesize'),
                        "url": f['url']
                    })
                elif f.get('acodec') != 'none' and f.get('vcodec') == 'none':
                    formats.append({
                        "format_id": f['format_id'],
                        "quality": "audio",
                        "ext": f.get('ext'),
                        "filesize": f.get('filesize'),
                        "url": f['url']
                    })
            return jsonify({
                "title": info.get('title'),
                "thumbnail": info.get('thumbnail'),
                "duration": info.get('duration'),
                "formats": formats
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
