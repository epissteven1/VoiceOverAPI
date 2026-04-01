from flask import Flask, request, send_file
from TTS.api import TTS
from io import BytesIO
import soundfile as sf

app = Flask(__name__)

# Initialize TTS model (CPU mode for Render)
tts_model = TTS(
    model_name="tts_models/en/vctk/vits",
    progress_bar=False,
    gpu=False
)

DEFAULT_SPEAKER = "p267"

@app.route("/tts", methods=["POST"])
def tts():
    data = request.get_json()

    if not data or "text" not in data:
        return {"error": "No text provided"}, 400

    text = data["text"]

    try:
        # Generate audio waveform (numpy array)
        audio = tts_model.tts(
            text=text,
            speaker=DEFAULT_SPEAKER
        )

        # Save to memory buffer
        audio_bytes = BytesIO()
        sf.write(audio_bytes, audio, samplerate=22050, format="WAV")
        audio_bytes.seek(0)

        # Return audio file
        return send_file(
            audio_bytes,
            mimetype="audio/wav",
            as_attachment=True,
            download_name="voice.wav"
        )

    except Exception as e:
        return {"error": str(e)}, 500


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
