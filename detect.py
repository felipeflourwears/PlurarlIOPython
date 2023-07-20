import cv2
import os
import requests
import json
import time

# Obtener la ruta completa del clasificador de cascada
script_dir = os.path.dirname(os.path.abspath(__file__))
cascade_path = os.path.join(script_dir, 'haarcascade_frontalface_default.xml')

# URL del endpoint para enviar la solicitud POST
url = "URL"

# Token de autorización para la solicitud POST
token = "YourToken"

# Verificar si el archivo del clasificador de cascada existe
if not os.path.isfile(cascade_path):
    raise FileNotFoundError(f"Error: No se pudo encontrar el archivo 'haarcascade_frontalface_default.xml' en la carpeta del script.")
else:
    print('PathReconocidoCascada')

# Cargar el clasificador de cascada
face_cascade = cv2.CascadeClassifier(cascade_path)

# Inicializar la cámara (usualmente la cámara 0 es la predeterminada)
cap = cv2.VideoCapture(1)

# Inicializar el temporizador
last_request_time = 0
min_time_interval = 60  # Intervalo mínimo entre solicitudes en segundos (1 minuto)

while True:
    # Capturar fotograma por fotograma desde la cámara
    ret, frame = cap.read()

    if not ret:
        break

    # Convertir a escala de grises para la detección de rostros
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detectar rostros en el fotograma
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4, minSize=(30, 30))

    # Dibujar rectángulo alrededor de los rostros detectados
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

     # Verificar si se detectó una cara
        if len(faces) > 0:
            flag = "Detect Face"
            num_faces_detected = len(faces)
            # Imprimir el número de caras detectadas y pausar la ejecución durante 1 segundo
        else:
            flag = "Undetect Face"
    

        # Obtener el tiempo actual
        current_time = time.time()

        # Verificar si ha pasado el tiempo suficiente desde la última solicitud
        if current_time - last_request_time >= min_time_interval:
            headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': 'Token ' + token  # Espacio después de 'Bearer'
            }

            # Preparar los datos en formato JSON para la solicitud POST
            payload = {
                "flag": flag,
                "faces":num_faces_detected
            }

            # Enviar la solicitud POST
            response = requests.post(url, json=payload, headers=headers)

            # Verificar si la solicitud se realizó correctamente
            if response.status_code == 200:
                print("Solicitud enviada correctamente.")
            else:
                print(f"Error en la solicitud. Código de estado: {response.status_code}")

            # Actualizar el tiempo de la última solicitud
            last_request_time = current_time

    # Mostrar el fotograma con las detecciones
    cv2.imshow('Video', frame)

    # Salir del bucle si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar los recursos y cerrar las ventanas
cap.release()
cv2.destroyAllWindows()
