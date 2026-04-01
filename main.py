from flask import Flask, request, send_file
from TTS.api import TTS
from io import BytesIO

app = Flask(__name__)

# TTS model setup
tts_model = TTS(model_name="tts_models/en/vctk/vits")
DEFAULT_SPEAKER = "p267"

@app.route("/tts", methods=["POST"])
def tts():
    data = request.get_json()
    text = data.get("text", "")

    if not text:
        return {"error": "No text provided"}, 400

    # Generate TTS into memory
    audio_bytes = BytesIO()
    tts_model.tts_to_file(text=text, file_path=audio_bytes, speaker=DEFAULT_SPEAKER)
    audio_bytes.seek(0)

    # Return as binary for n8n
    return send_file(
        audio_bytes,
        mimetype="audio/mpeg",
        as_attachment=True,
        download_name="voice.mp3"
    )

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)