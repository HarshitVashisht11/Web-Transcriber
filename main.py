from flask import Flask, render_template, request, flash, send_file, redirect, url_for
import os
import whisper
import tempfile

import time

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp4', 'mp3', 'm4a', 'webm', 'mpga', 'mpeg', 'wav'}

LANGUAGES = {
    "en": "English",
    "zh": "Chinese",
    "de": "German",
    "es": "Spanish",
    "ru": "Russian",
    "ko": "Korean",
    "fr": "French",
    "ja": "Japanese",
    "pt": "Portuguese",
    "tr": "Turkish",
    "pl": "Polish",
    "ca": "Catalan",
    "nl": "Dutch",
    "ar": "Arabic",
    "sv": "Swedish",
    "it": "Italian",
    "id": "Indonesian",
    "hi": "Hindi",
    "fi": "Finnish",
    "vi": "Vietnamese",
    "he": "Hebrew",
    "uk": "Ukrainian",
    "el": "Greek",
    "ms": "Malay",
    "cs": "Czech",
    "ro": "Romanian",
    "da": "Danish",
    "hu": "Hungarian",
    "ta": "Tamil",
    "no": "Norwegian",
    "th": "Thai",
    "ur": "Urdu",
    "hr": "Croatian",
    "bg": "Bulgarian",
    "lt": "Lithuanian",
    "la": "Latin",
    "mi": "Maori",
    "ml": "Malayalam",
    "cy": "Welsh",
    "sk": "Slovak",
    "te": "Telugu",
    "fa": "Persian",
    "lv": "Latvian",
    "bn": "Bengali",
    "sr": "Serbian",
    "az": "Azerbaijani",
    "sl": "Slovenian",
    "kn": "Kannada",
    "et": "Estonian",
    "mk": "Macedonian",
    "br": "Breton",
    "eu": "Basque",
    "is": "Icelandic",
    "hy": "Armenian",
    "ne": "Nepali",
    "mn": "Mongolian",
    "bs": "Bosnian",
    "kk": "Kazakh",
    "sq": "Albanian",
    "sw": "Swahili",
    "gl": "Galician",
    "mr": "Marathi",
    "pa": "Punjabi",
    "si": "Sinhala",
    "km": "Khmer",
    "sn": "Shona",
    "yo": "Yoruba",
    "so": "Somali",
    "af": "Afrikaans",
    "oc": "Occitan",
    "ka": "Georgian",
    "be": "Belarusian",
    "tg": "Tajik",
    "sd": "Sindhi",
    "gu": "Gujarati",
    "am": "Amharic",
    "yi": "Yiddish",
    "lo": "Lao",
    "uz": "Uzbek",
    "fo": "Faroese",
    "ht": "Haitian creole",
    "ps": "Pashto",
    "tk": "Turkmen",
    "nn": "Nynorsk",
    "mt": "Maltese",
    "sa": "Sanskrit",
    "lb": "Luxembourgish",
    "my": "Myanmar",
    "bo": "Tibetan",
    "tl": "Tagalog",
    "mg": "Malagasy",
    "as": "Assamese",
    "tt": "Tatar",
    "haw": "Hawaiian",
    "ln": "Lingala",
    "ha": "Hausa",
    "ba": "Bashkir",
    "jw": "Javanese",
    "su": "Sundanese",
    "yue": "Cantonese",
}

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
    return render_template("index.html",LANGUAGES=LANGUAGES)

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

            time.sleep(2)

            transcript_path = process_file(file_path, model_type, language)

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

def run_app():
    app.run(debug=True)

if __name__ == '__main__':
    run_app()
