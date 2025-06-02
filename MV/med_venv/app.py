from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename

from utils.image_predict import predict_image
from utils.llm import generate_response
from utils.asr import transcribe_audio  # Assuming you have this utility

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'static/uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Save uploaded image
        image_file = request.files.get('image')
        audio_file = request.files.get('audio')
        symptom_text = request.form.get('symptom_text', '').strip()

        if not image_file:
            return render_template('index.html', result="Please upload an X-ray image.")

        image_filename = secure_filename(image_file.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
        image_file.save(image_path)

        # Predict X-ray result
        label = predict_image(image_path)

        # Transcribe audio if provided
        if audio_file and audio_file.filename != '':
            audio_filename = secure_filename(audio_file.filename)
            audio_path = os.path.join(app.config['UPLOAD_FOLDER'], audio_filename)
            audio_file.save(audio_path)
            try:
                symptoms = transcribe_audio(audio_path)
            except Exception as e:
                symptoms = ''
        else:
            symptoms = ''

        # If user typed symptoms, override audio transcription
        if symptom_text:
            symptoms = symptom_text

        # Generate medical suggestion based on prediction and symptoms
        suggestion = generate_response(symptoms, label)

        # Pass result and image filename to template
        return render_template('index.html', result=f"{label.capitalize()}: {suggestion}", image=f"uploads/{image_filename}")

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
