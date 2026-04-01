from flask import Flask, request, send_file
from TTS.api import TTS
import uuid
import os

app = Flask(__name__)

OUTPUT_DIR = "audio"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Initialize the TTS model once at startup
# Always use p267 as the speaker
tts_model = TTS(model_name="tts_models/en/vctk/vits")  
DEFAULT_SPEAKER = "p267"

@app.route("/tts", methods=["POST"])
def tts():
    data = request.get_json()
    text = data.get("text", "")

    if not text:
        return {"error": "No text provided"}, 400

    filename = f"{uuid.uuid4()}.mp3"
    filepath = os.path.join(OUTPUT_DIR, filename)

    # Always generate TTS with p267
    tts_model.tts_to_file(text=text, file_path=filepath, speaker=DEFAULT_SPEAKER)

    return send_file(filepath, as_attachment=True)

@app.route("/voices", methods=["GET"])
def voices():
    """Return a list of available speakers for this model."""
    return {"voices": tts_model.speakers, "default": DEFAULT_SPEAKER}

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port) 