"""
Small launcher to run the Flask app and open the default browser.
Use this script when packaging into a single-file EXE with PyInstaller.
"""
import webbrowser
import time

# Import the Flask app object from the application module
# Prefer importing the Flask app instance directly so calling `run()` works
try:
    # Common pattern: word_to_audio/app.py exposes `app = Flask(__name__)`
    from word_to_audio.app import app
except Exception:
    # Fall back to attempting to import the package attribute (older packaging setups)
    # This helps in environments where the package exposes the module as an attribute.
    from word_to_audio import app  # type: ignore

def _open_browser_later(url: str, delay: float = 0.8):
    try:
        import threading
        def _open():
            time.sleep(delay)
            try:
                webbrowser.open(url)
            except Exception:
                pass
        t = threading.Thread(target=_open, daemon=True)
        t.start()
    except Exception:
        # best-effort only; ignore if threading isn't available
        try:
            time.sleep(delay)
            webbrowser.open(url)
        except Exception:
            pass

if __name__ == '__main__':
    port = 5000
    url = f'http://127.0.0.1:{port}/'
    # try to open browser after a short delay so the server can start
    _open_browser_later(url)

    # Run Flask app (app should be the Flask application instance)
    # Bind to localhost so the EXE only serves locally
    try:
        app.run(host='127.0.0.1', port=port, debug=False)
    except AttributeError:
        # Provide a clearer error if `app` isn't the Flask instance
        raise RuntimeError(
            "Imported `app` from 'word_to_audio' does not expose a run() method.\n"
            "Ensure `word_to_audio/app.py` defines `app = Flask(__name__)` and that you import it via ``from word_to_audio.app import app``."
        )
"""
Small launcher to run the Flask app and open the default browser.
Use this script when packaging into a single-file EXE with PyInstaller.
"""
import webbrowser
import time

# Import the Flask app module
from word_to_audio import app

if __name__ == '__main__':
    port = 5000
    url = f'http://127.0.0.1:{port}/'
    # Open browser after a tiny delay so server can start
    def open_browser_later():
        time.sleep(0.8)
        try:
            webbrowser.open(url)
        except Exception:
            pass

    # Start browser opener in a thread to avoid blocking
    try:
        import threading
        t = threading.Thread(target=open_browser_later, daemon=True)
        t.start()
    except Exception:
        pass

    # Run Flask app (app object imported from word_to_audio.app)
    # Bind to localhost so the EXE only serves locally
    app.run(host='127.0.0.1', port=port, debug=False)
