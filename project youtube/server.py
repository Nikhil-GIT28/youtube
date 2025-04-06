from flask import Flask, render_template, request, send_file
from pytube import YouTube
import os
from datetime import datetime

app = Flask(__name__)

# Configuration
DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/')
def home():
    return render_template('youtube.html')

@app.route('/download', methods=['POST'])
def download_video():
    url = request.form.get('yt_url')
    try:
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        
        # Sanitize filename
        safe_title = "".join(c for c in yt.title if c.isalnum() or c in " _-")
        filename = f"{safe_title}.mp4"
        filepath = os.path.join(DOWNLOAD_FOLDER, filename)
        
        # Download and send
        stream.download(output_path=DOWNLOAD_FOLDER, filename=filename)
        return send_file(filepath, as_attachment=True, download_name=filename)
        
    except Exception as e:
        return f"Error: {str(e)}", 400

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
