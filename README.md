# DocuVoice — Text & Word to Audio Web App

A small Flask web app that converts typed text and uploaded Word (.docx) documents to audio (MP3) using Google Text-to-Speech (gTTS), and also saves browser-recorded audio. The app stores uploaded files in `uploads/` and generated audio in `audio_files/`.

## Key features

- Convert plain text to MP3 audio
- Upload a Word (.docx) document and convert its text to MP3
- Save voice recordings uploaded from the browser
- Organized output: `audio_files/<module>/` (timestamped filenames)

## Project layout (important files/folders)

- `word_to_audio/app.py` — main Flask application (routes and conversion logic)
- `audio_files/` — generated audio files are saved here, organized by module
- `uploads/` — uploaded Word files are stored here before conversion
- `templates/` — HTML templates used by the Flask app (index, text_to_speech, word_to_speech, voice_recording)
- `static/` — CSS and frontend assets (e.g. `styles.css`)

> Note: The Flask app uses `render_template` for `index.html`, `text_to_speech.html`, etc. Ensure these exact filenames exist inside `templates/`.

## Requirements

- Python 3.8+ recommended
- pip
- Windows PowerShell (examples below target PowerShell)

Python packages used by the app (as seen in `word_to_audio/app.py`):

- Flask
- gTTS
- python-docx

You can install these packages manually or create a small `requirements.txt`:

```
Flask
gTTS
python-docx
```

Install with pip:

```powershell
# create and activate a virtual environment (recommended)
python -m venv .venv; .\.venv\Scripts\Activate.ps1

# install dependencies
pip install -r requirements.txt
```

### Additional system requirements for local hosting

- If you plan to use `pydub` to concatenate audio parts, install `ffmpeg` on your machine and ensure it's in your PATH. On Windows, download a static build from https://ffmpeg.org/download.html and add the `bin` directory to your PATH.

---

## Hosting locally and connecting from another device (LAN)

These steps let you run the Flask app on your machine and access it from other devices on the same local network.

1. Ensure your machine and the other device are on the same Wi‑Fi or LAN.
2. In PowerShell, create and activate the venv and install dependencies:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

3. Start the Flask app bound to all interfaces so other devices can reach it. From the project root run:

```powershell
# Option A: run the app directly (if app.py calls app.run())
python .\word_to_audio\app.py

# Option B: use Flask CLI (recommended for development)
$env:FLASK_APP = 'word_to_audio.app'; $env:FLASK_ENV = 'development'
python -m flask run --host=0.0.0.0 --port=5000
```

4. Find your PC's local IP address (IPv4). In PowerShell:

```powershell
ipconfig
```

Look for the IPv4 Address under the active network adapter (e.g., `192.168.1.42`).

5. From another device on the same network, open a browser and visit:

```
http://<YOUR_LOCAL_IP>:5000/
```

Example: `http://192.168.1.42:5000/`

6. Windows firewall: if you can't reach the app from another device, allow inbound traffic on the port (5000) with an elevated PowerShell prompt:

```powershell
# Run as Administrator
New-NetFirewallRule -DisplayName "Allow Flask 5000" -Direction Inbound -LocalPort 5000 -Protocol TCP -Action Allow
```

7. Router/Internet access: exposing your app to the public internet requires additional steps (port forwarding, static IP or DNS, TLS). I strongly recommend using a secure tunnel (for example, `ngrok`) for temporary external access instead of exposing your machine directly.

Security note: running a development Flask server on `0.0.0.0` is fine for testing on a trusted LAN. Do not use the development server for production; consider deploying to a proper WSGI server (Gunicorn, uWSGI) behind a reverse proxy for production use.


## How to run (development)

There are two easy ways to run the app on Windows/PowerShell.

1) Run with Python directly (works because `app.py` calls `app.run()`):

```powershell
# from project root
python .\word_to_audio\app.py
```

2) Use Flask CLI (optional):

```powershell
# set FLASK_APP and run (PowerShell syntax)
$env:FLASK_APP = 'word_to_audio.app'; $env:FLASK_ENV = 'development'
python -m flask run
```

Open your browser at http://127.0.0.1:5000/ (or the address shown in console).

## How to use

- Text-to-Speech: paste or type text on the Text-to-Speech page and submit. The app will generate an MP3 in `audio_files/text_to_speech/` with a timestamped filename.
- Word-to-Speech: upload a `.docx` file on the Word-to-Speech page. The server saves the upload in `uploads/`, extracts the text, and creates an MP3 under `audio_files/word_to_speech/`.
- Voice Recording: record audio from the browser UI (if implemented in the frontend) and submit; the file is saved under `audio_files/voice_recording/` as a WAV.

Generated filenames include a timestamp: `<module>_..._YYYYMMDD_HHMMSS.ext`.

## Notes & troubleshooting

- Templates: The Flask code renders `index.html` and other `*.html` templates. If your template files are named with different casing (e.g. `INDEX.html`) or located in a different path, rename or move them to `templates/index.html`, etc.
- Ports and binding: By default Flask runs on port 5000 and binds to `127.0.0.1`. Use `app.run(host='0.0.0.0')` if you need external access (be cautious in production).
- gTTS: The Google TTS library requires network access to fetch synthesized audio. Ensure your system has internet access when generating speech.
- File permissions: Ensure Python can write to `uploads/` and `audio_files/`. The app tries to create these directories automatically.
- Large documents: Very large `.docx` files may take time to convert and may hit rate limits on gTTS; consider splitting text for very large inputs.

## Next steps / improvements (optional)

- Add a `requirements.txt` and/or `pyproject.toml` for reproducible installs.
- Add a simple UI element that lists generated audio files with download links.
- Add basic tests for the conversion functions (unit tests for `convert_word_to_text` and `convert_text_to_audio`).
- Add error handling and user feedback for long-running conversions.

## License

Add a license file if you plan to share the project publicly (e.g., `MIT`).

---

If you want, I can also:
- create a `requirements.txt` with pinned versions,
- add a small health/check route or a download page for generated audio,
- or update template filenames if there's a mismatch between template names and the code. Just tell me which you'd like next.