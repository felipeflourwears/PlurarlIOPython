import requests
import json

# URL del endpoint para enviar la solicitud POST
url = "URL"

# Token de autorización para la solicitud POST
token = "YourToken"

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': 'Token ' + token  # Espacio después de 'Bearer'
}

# JSON con la estructura clave-valor
jsons = {"key": "value"}

response = requests.post(url, json=jsons, headers=headers)

# Comprobar el resultado de la solicitud
if response.status_code == 200:
    print("Solicitud exitosa!")
    print(response.json())
else:
    print("Error en la solicitud:", response.status_code)
