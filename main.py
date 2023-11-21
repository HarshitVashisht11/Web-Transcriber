from flask import Flask, render_template, request, flash, send_file, redirect, url_for
import os
import whisper
import tempfile
import time

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp4', 'mp3', 'm4a', 'webm', 'mpga', 'mpeg', 'wav'}

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_file(file_path, model_type, language):
    print(f"The language is {language}, model is {model_type}, and filename is {file_path}")

    model = whisper.load_model(model_type)
    audio = whisper.load_audio(file_path)
    result = model.transcribe(audio, language=language)
    print(result)

    transcript_path = save_transcript(result['text'])
    return transcript_path

def save_transcript(transcript_text):
    temp_dir = tempfile.mkdtemp()
    transcript_path = os.path.join(temp_dir, 'transcript.txt')

    with open(transcript_path, 'w', encoding='utf-8') as file:
        file.write(transcript_text)

    return transcript_path

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/transcribe", methods=['POST'])
def transcribe():
    try:
        audio_file = request.files['audioFile']
        language = request.form['language']
        model_type = request.form['model']

        if audio_file and allowed_file(audio_file.filename):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], audio_file.filename)
            audio_file.save(file_path)

            flash('Transcribing audio. Please wait...', 'info')

            # Simulating a delay for demonstration purposes
            time.sleep(2)

            transcript_path = process_file(file_path, model_type, language)

            # Render the result.html template directly
            with open(transcript_path, 'r', encoding='utf-8') as file:
                transcript_text = file.read()

            return render_template("result.html", result={'language': language, 'text': transcript_text, 'transcript_path': transcript_path})

        else:
            flash('Invalid file format. Please upload an allowed audio file.', 'danger')
    except Exception as e:
        print(str(e))
        flash('Error during transcription. Please try again.', 'danger')

    return redirect(url_for('hello_world'))  # Redirect to the home page if there's an issue

@app.route("/download")
def download_transcription():
    transcript_path = request.args.get('transcript_path', default='', type=str)

    if not transcript_path:
        flash('Error loading transcription result. Please try again.', 'danger')
        return redirect(url_for('hello_world'))

    return send_file(transcript_path, as_attachment=True)

@app.route("/features")
def features():
    return render_template("features.html")

if __name__ == '__main__':
    app.run(debug=True)
