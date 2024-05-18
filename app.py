from flask import Flask, request, jsonify, send_from_directory
import whisper
import pandas as pd
import os

app = Flask(__name__)

model = whisper.load_model("base")

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    audio_file = request.files['audio']
    audio_path = os.path.join("uploads", audio_file.filename)
    audio_file.save(audio_path)
    
    result = model.transcribe(audio_path)
    transcription_text = result["text"]
    
    os.remove(audio_path)  # Eliminar el archivo después de la transcripción
    return jsonify({'transcription': transcription_text})

@app.route('/standardize', methods=['POST'])
def standardize_text():
    data = request.json
    schedule_text = data.get('schedule_text')
    response = client.Completion.create(
        engine="text-davinci-002",
        prompt=f"Standardize the following schedule:\n{schedule_text}",
        max_tokens=150
    )
    standardized_text = response.choices[0].text.strip()
    return jsonify({'standardized_text': standardized_text})

@app.route('/create_schedule', methods=['POST'])
def create_schedule_table():
    data = request.json
    schedule_text = data.get('schedule_text')
    rows = schedule_text.split('\n')
    data = [row.split(' ') for row in rows]
    df = pd.DataFrame(data, columns=['Hora de Inicio', 'Hora de Fin', 'Actividad'])
    df.to_excel('horario.xlsx', index=False)
    return jsonify({'message': 'Schedule created successfully', 'file_path': 'horario.xlsx'})

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
