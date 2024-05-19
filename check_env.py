import os

api_key = os.getenv('OPENAI_API_KEY')

if api_key:
    print("La API Key se ha cargado correctamente.")
else:
    print("No se ha encontrado la API Key. Asegúrate de que esté configurada correctamente.")
