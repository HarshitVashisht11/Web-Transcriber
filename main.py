from flask import Flask, render_template, request, flash, send_file
import os
import whisper
import tempfile

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

    # Load Whisper model
    model = whisper.load_model(model_type)

    # Load audio
    audio = whisper.load_audio(file_path)

    # Transcribe audio
    result = model.transcribe(audio)
    print(result)

    # Save transcript to a text file
    transcript_path = save_transcript(result['text'])
    return transcript_path

def save_transcript(transcript_text):
    # Create a temporary directory to store transcript files
    temp_dir = tempfile.mkdtemp()
    transcript_path = os.path.join(temp_dir, 'transcript.txt')

    # Write transcript to the file
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
            # Save the uploaded file
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], audio_file.filename)
            audio_file.save(file_path)

            # Process the uploaded file
            transcript_path = process_file(file_path, model_type, language)

            flash('Transcription successful!', 'success')
            return send_file(transcript_path, as_attachment=True)

        else:
            flash('Invalid file format. Please upload an allowed audio file.', 'danger')
    except Exception as e:
        print(str(e))
        flash('Error during transcription. Please try again.', 'danger')

    return render_template("index.html")

if __name__ == '__main__':
   app.run(debug=True)
