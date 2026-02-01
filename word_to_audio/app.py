from flask import Flask, render_template, request, send_from_directory, redirect, url_for, jsonify
import threading
import uuid
import time
import os
import socket
from gtts import gTTS
from docx import Document
import datetime

# Optional: zeroconf (mDNS) announcer so the app can be discovered as a .local name on the LAN
try:
    from zeroconf import ServiceInfo, Zeroconf
    ZEROCONF_AVAILABLE = True
except Exception:
    ZEROCONF_AVAILABLE = False

# Optional: use pydub to concatenate per-paragraph MP3s into one final MP3
try:
    from pydub import AudioSegment
    PYDUB_AVAILABLE = True
except Exception:
    PYDUB_AVAILABLE = False

app = Flask(__name__)


@app.context_processor
def inject_current_year():
    from datetime import datetime
    return {'current_year': datetime.now().year}

# Folder to store uploaded files and audio files
UPLOAD_FOLDER = 'uploads'
AUDIO_FOLDER = 'audio_files'
                                                            
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['AUDIO_FOLDER'] = AUDIO_FOLDER

# Ensure the folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(AUDIO_FOLDER, exist_ok=True)

# Simple in-memory job store for background conversions
JOBS = {}
JOBS_LOCK = threading.Lock()

def convert_word_to_text(word_file):
    """Convert Word file content to text."""
    doc = Document(word_file)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

def convert_text_to_audio(text, module_name):
    """Convert text to audio and save it as an MP3 file with a timestamp."""
    tts = gTTS(text=text, lang='en')
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    audio_filename = f"{module_name}_text_to_audio_{timestamp}.mp3"
    
    # Create subfolder for the module if not exists
    module_folder = os.path.join(AUDIO_FOLDER, module_name)
    os.makedirs(module_folder, exist_ok=True)
    
    audio_path = os.path.join(module_folder, audio_filename)
    tts.save(audio_path)  # Save the audio file with timestamp
    return audio_path


def _start_background_conversion(job_id, word_file, module_name):
    """Background worker that converts a Word file to audio and updates JOBS progress."""
    try:
        # Read document and split into parts to allow incremental progress
        with JOBS_LOCK:
            JOBS[job_id]['progress'] = 3
            JOBS[job_id]['message'] = 'Reading document'

        text = convert_word_to_text(word_file)

        # split into paragraphs (non-empty lines)
        parts = [p.strip() for p in text.splitlines() if p.strip()]
        if not parts:
            parts = [text.strip()]

        total_parts = max(1, len(parts))

        # Estimate work based on file size + number of parts
        try:
            file_size = os.path.getsize(word_file)
        except Exception:
            file_size = 0

        with JOBS_LOCK:
            JOBS[job_id]['progress'] = 8
            JOBS[job_id]['message'] = f'Preparing {total_parts} parts'
            JOBS[job_id]['detail'] = f'0/{total_parts}'

        # create module folder and temporary folder for parts
        module_folder = os.path.join(AUDIO_FOLDER, module_name)
        os.makedirs(module_folder, exist_ok=True)
        tmp_folder = os.path.join(module_folder, f"tmp_{job_id}")
        os.makedirs(tmp_folder, exist_ok=True)

        part_files = []

        # Generate per-part audio and update progress gradually
        for idx, part in enumerate(parts):
            with JOBS_LOCK:
                JOBS[job_id]['message'] = f'Generating part {idx+1}/{total_parts}'
                JOBS[job_id]['detail'] = f'{idx+1}/{total_parts}'

            # generate MP3 for this part
            try:
                part_tts = gTTS(text=part, lang='en')
                part_path = os.path.join(tmp_folder, f"{job_id}_{idx}.mp3")
                part_tts.save(part_path)
                part_files.append(part_path)
            except Exception as e:
                with JOBS_LOCK:
                    JOBS[job_id]['status'] = 'error'
                    JOBS[job_id]['message'] = f'Error generating part: {str(e)}'
                    JOBS[job_id]['progress'] = 100
                return

            # update progress: map parts generation into 10..85 range
            made = idx + 1
            progress = 8 + int((made / total_parts) * 77)
            with JOBS_LOCK:
                JOBS[job_id]['progress'] = min(progress, 95)

        # Combine parts into final MP3
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        audio_filename = f"{module_name}_word_to_audio_{timestamp}.mp3"
        audio_path = os.path.join(module_folder, audio_filename)

        if PYDUB_AVAILABLE and part_files:
            try:
                combined = None
                for pf in part_files:
                    seg = AudioSegment.from_file(pf, format='mp3')
                    if combined is None:
                        combined = seg
                    else:
                        combined += seg
                if combined is None:
                    raise RuntimeError('No parts to combine')
                combined.export(audio_path, format='mp3')
            except Exception as e:
                # fallback: create single file from full text
                try:
                    audio_path = convert_text_to_audio(text, module_name)
                except Exception as ee:
                    with JOBS_LOCK:
                        JOBS[job_id]['status'] = 'error'
                        JOBS[job_id]['message'] = f'Error combining parts: {str(e)}; fallback failed: {str(ee)}'
                        JOBS[job_id]['progress'] = 100
                    return
        else:
            # pydub not available, perform single-shot TTS as fallback
            try:
                audio_path = convert_text_to_audio(text, module_name)
            except Exception as e:
                with JOBS_LOCK:
                    JOBS[job_id]['status'] = 'error'
                    JOBS[job_id]['message'] = f'Error generating audio: {str(e)}'
                    JOBS[job_id]['progress'] = 100
                return

        # remove temporary part files
        try:
            for pf in part_files:
                if os.path.exists(pf):
                    os.remove(pf)
            if os.path.isdir(tmp_folder):
                os.rmdir(tmp_folder)
        except Exception:
            pass

        with JOBS_LOCK:
            JOBS[job_id]['progress'] = 96
            JOBS[job_id]['message'] = 'Finalizing'
            JOBS[job_id]['audio_path'] = audio_path

        # small pause so frontend can reach 100% visibly
        time.sleep(0.5)

        with JOBS_LOCK:
            JOBS[job_id]['progress'] = 100
            JOBS[job_id]['status'] = 'done'
            JOBS[job_id]['message'] = 'Completed'

    except Exception as e:
        with JOBS_LOCK:
            JOBS[job_id]['status'] = 'error'
            JOBS[job_id]['message'] = f'Error: {str(e)}'
            JOBS[job_id]['progress'] = 100

    finally:
        # Optionally remove the uploaded word file to save space
        try:
            if os.path.exists(word_file):
                os.remove(word_file)
        except Exception:
            pass

@app.route("/", methods=["GET"])
def home():
    """Home page with options to navigate to either text-to-speech, word-to-speech, or voice recording."""
    return render_template("index.html")


@app.route("/text-to-speech", methods=["GET"])
def text_to_speech_page():
    """Page to convert text to speech."""
    return render_template("text_to_speech.html")


@app.route("/word-to-speech", methods=["GET"])
def word_to_speech_page():
    """Page to upload Word file and convert it to speech."""
    return render_template("word_to_speech.html")


@app.route("/voice-recording", methods=["GET"])
def voice_recording_page():
    """Page for voice recording."""
    return render_template("voice_recording.html")


@app.route("/text-to-audio", methods=["POST"])
def text_to_audio():
    """Route to handle text-to-speech conversion."""
    text = request.form['text']
    module_name = 'text_to_speech'  # Name of the module to save in the folder

    # Convert text to audio
    audio_path = convert_text_to_audio(text, module_name)

    # After saving the audio, show a success animation then redirect to home
    return render_template('success.html', message='Text converted to audio', redirect_url=url_for('home'), delay_ms=1500)


@app.route("/word-to-audio", methods=["POST"])
def word_to_audio():
    """Route to handle Word file upload and conversion to audio."""
    file = request.files['file']
    if file and file.filename.endswith('.docx'):
        # ensure a unique filename to avoid collisions
        unique_name = f"{uuid.uuid4().hex}_{file.filename}"
        word_file_path = os.path.join(UPLOAD_FOLDER, unique_name)
        file.save(word_file_path)

        module_name = 'word_to_speech'  # Name of the module to save in the folder

        # Create a job and start background worker
        job_id = uuid.uuid4().hex
        with JOBS_LOCK:
            JOBS[job_id] = {
                'status': 'pending',
                'progress': 0,
                'message': 'Queued',
                'audio_path': None,
            }
        app.logger.info(f"Created job {job_id} for {word_file_path}")

        worker = threading.Thread(target=_start_background_conversion, args=(job_id, word_file_path, module_name), daemon=True)
        worker.start()

        # Render a processing page that will poll the job status
        return render_template('processing.html', job_id=job_id)


@app.route("/save-voice", methods=["POST"])
def save_voice():
    """Save the recorded audio from the browser."""
    file = request.files['file']
    if file:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        module_name = 'voice_recording'  # Name of the module to save in the folder
        voice_filename = f"{module_name}_voice_recording_{timestamp}.wav"

        # Create subfolder for voice recordings
        module_folder = os.path.join(AUDIO_FOLDER, module_name)
        os.makedirs(module_folder, exist_ok=True)

        file_path = os.path.join(module_folder, voice_filename)
        file.save(file_path)

        # After saving the voice recording, show a success animation then redirect to home
        return render_template('success.html', message='Voice recording saved', redirect_url=url_for('home'), delay_ms=1500)

    return jsonify({'message': 'Failed to save audio'}), 400





@app.route('/job-status/<job_id>', methods=['GET'])
def job_status(job_id):
    app.logger.info(f"job_status requested for {job_id}")
    with JOBS_LOCK:
        job = JOBS.get(job_id)
        # log current job keys for easier debugging
        app.logger.info(f"Current jobs: {list(JOBS.keys())}")
        if not job:
            # return a 200 with a notfound state so client JS can handle it gracefully
            return jsonify({'status': 'notfound', 'message': 'Job not found or expired', 'progress': 0}), 200
        return jsonify({
            'status': job.get('status'),
            'progress': job.get('progress', 0),
            'message': job.get('message', ''),
            'detail': job.get('detail', '')
        })


def _get_local_ip():
    """Return the machine's local LAN IP address (best-effort)."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # This does not send data; it just determines the outbound interface.
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        try:
            s.close()
        except Exception:
            pass
    return ip


@app.route('/local-ip', methods=['GET'])
def local_ip():
    """Return the detected local IP as JSON for client-side usage."""
    ip = _get_local_ip()
    return jsonify({'ip': ip})


@app.route('/_debug-jobs', methods=['GET'])
def debug_jobs():
    """Debug-only endpoint that returns current jobs and statuses."""
    with JOBS_LOCK:
        return jsonify({k: {'status': v.get('status'), 'progress': v.get('progress')} for k, v in JOBS.items()})


@app.route('/success-redirect/<job_id>', methods=['GET'])
def success_redirect(job_id):
    # After job completes, show success animation and then redirect home
    with JOBS_LOCK:
        job = JOBS.get(job_id)
        if not job:
            return redirect(url_for('home'))
        msg = job.get('message', 'Completed')
    return render_template('success.html', message='Conversion complete', redirect_url=url_for('home'), delay_ms=1400)


if __name__ == "__main__":
    # Allow configuring host and port via environment variables so the server
    # can be bound to the LAN address (0.0.0.0) for access from other devices.
    host = os.environ.get('DOCUVOICE_HOST', '0.0.0.0')
    try:
        port = int(os.environ.get('DOCUVOICE_PORT', '5000'))
    except Exception:
        port = 5000
    debug_env = os.environ.get('DOCUVOICE_DEBUG', '')
    debug = True if debug_env.lower() in ('1', 'true', 'yes') else False

    app.logger.info(f"Starting DocuVoice on {host}:{port} (debug={debug})")

    # Optional: advertise via mDNS/zeroconf if requested and available
    mdns_enabled = os.environ.get('DOCUVOICE_MDNS', '').lower() in ('1', 'true', 'yes')
    mdns_name = os.environ.get('DOCUVOICE_MDNS_NAME', 'docuvoice')
    if mdns_enabled:
        if ZEROCONF_AVAILABLE:
            def _register_mdns():
                try:
                    zc = Zeroconf()
                    # Service name: <name>._http._tcp.local.
                    service_name = f"{mdns_name}._http._tcp.local."
                    info = ServiceInfo(
                        "_http._tcp.local.",
                        service_name,
                        addresses=[socket.inet_aton(host if host != '0.0.0.0' else '127.0.0.1')],
                        port=port,
                        properties={"path": "/"},
                        server=f"{mdns_name}.local.",
                    )
                    zc.register_service(info)
                    app.logger.info(f"mDNS: Registered service {service_name} on port {port}")
                except Exception as e:
                    app.logger.warning(f"mDNS registration failed: {e}")
        else:
            app.logger.info('DOCUVOICE_MDNS requested but zeroconf package is not available. Install `zeroconf` to enable mDNS announcement.')

    # Optional SSL: allow specifying certificate and key via environment variables
    ssl_cert = os.environ.get('DOCUVOICE_CERT')
    ssl_key = os.environ.get('DOCUVOICE_KEY')
    ssl_context = None
    if ssl_cert and ssl_key and os.path.exists(ssl_cert) and os.path.exists(ssl_key):
        ssl_context = (ssl_cert, ssl_key)
        app.logger.info(f"SSL enabled using cert={ssl_cert} key={ssl_key}")
    else:
        if ssl_cert or ssl_key:
            app.logger.warning('DOCUVOICE_CERT/DOCUVOICE_KEY were set but cert or key file not found; continuing without SSL.')

    # If mdns was enabled and zeroconf is available, register in a background thread
    if mdns_enabled and ZEROCONF_AVAILABLE:
        t = threading.Thread(target=_register_mdns, daemon=True)
        t.start()

    app.run(host=host, port=port, debug=debug, ssl_context=ssl_context)
