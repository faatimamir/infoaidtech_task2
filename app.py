from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
import os
from google.cloud import speech_v1p1beta1 as speech

app = Flask(__name__)

# Replace 'your-google-credentials.json' with your actual Google Cloud credentials file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "your-google-credentials.json"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/record', methods=['POST'])
def record():
    try:
        recognizer = sr.Recognizer()
        
        with sr.Microphone() as source:
            print("Recording...")
            audio_data = recognizer.listen(source, timeout=5)
            print("Recording complete.")

        # Transcribe using Google Speech-to-Text
        client = speech.SpeechClient()
        audio = speech.RecognitionAudio(content=audio_data.frame_data)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code="en-US",
        )

        response = client.recognize(config=config, audio=audio)
        transcription_result = response.results[0].alternatives[0].transcript

        return jsonify({'transcription': transcription_result})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
