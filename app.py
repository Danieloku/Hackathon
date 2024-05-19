from flask import Flask, request, jsonify, send_from_directory
import openai
import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Configurar la API Key de OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

if not openai.api_key:
    raise ValueError("La API Key de OpenAI no está configurada. Por favor, configúrala como una variable de entorno.")

app = Flask(__name__)

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    try:
        audio_file = request.files['audio']
        
        # Crear la transcripción usando la API de OpenAI
        response = openai.Audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="text"
        )
        transcription_text = response['text']
        return jsonify({'transcription': transcription_text})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/standardize', methods=['POST'])
def standardize_text():
    data = request.json
    schedule_text = data.get('schedule_text')
    response = openai.Completion.create(
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
