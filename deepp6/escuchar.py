import sounddevice as sd
import numpy as np
import vosk
import json

def escuchar_comando():
    """
    Captura audio desde el micrófono, lo procesa utilizando el modelo Vosk y
    retorna el comando reconocido como texto.
    """
    try:
        # Cargar el modelo de Vosk
        print("Cargando modelo de Vosk...")
        model = vosk.Model("vosk-model-small-es-0.42")  # Ajusta la ruta si el modelo está en otro lugar
        rec = vosk.KaldiRecognizer(model, 16000)  # Frecuencia de muestreo: 16 kHz

        fs = 16000  # Frecuencia de muestreo
        duration = 5  # Duración de la grabación en segundos

        print("Escuchando...")
        # Grabar audio del micrófono
        audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()  # Esperar a que se complete la grabación
        print("Grabación finalizada. Procesando...")

        # Convertir el audio a bytes
        audio_bytes = audio.tobytes()

        # Procesar el audio con Vosk
        if rec.AcceptWaveform(audio_bytes):
            result = rec.Result()  # Resultado completo si el audio fue reconocido
        else:
            result = rec.PartialResult()  # Resultado parcial si no se pudo reconocer completamente

        # Convertir el resultado a un diccionario
        result_dict = json.loads(result)

        # Extraer el comando del texto reconocido
        comando = result_dict.get('text', None)
        if comando:
            print(f"Comando recibido: {comando}")
        else:
            #comando = ""
            print("No se entendió el comando.")
        
        return comando
    except Exception as e:
        print(f"Error durante el reconocimiento de voz: {e}")
        return ""
    

import speech_recognition as sr






def escuchar_comando3(microphone_lock):
    r = sr.Recognizer()
    with microphone_lock:  # Bloquea el acceso al micrófono
        with sr.Microphone() as source:
            print("Escuchando...")
            audio = r.listen(source)

    try:
        comando = r.recognize_google(audio, language='es-ES')
        print(f"Comando recibido: {comando}")
        return comando
    except sr.UnknownValueError:
        print("No se entendió el comando.")
        return None
    except sr.RequestError as e:
        print(f"No se pudo conectar al servicio de reconocimiento de voz: {e}")
        return None


def escuchar_comando0():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Escuchando...")
        audio = r.listen(source)

    try:
        comando = r.recognize_google(audio, language='es-ES')
        print(f"Comando recibido: {comando}")
        return comando
    except sr.UnknownValueError:
        print("No se entendió el comando.")
        return None
    except sr.RequestError as e:
        print(f"No se pudo conectar al servicio de reconocimiento de voz: {e}")
        return None


def grabar_audio_durante_10_seg():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Grabando audio durante 10 segundos... Habla ahora.")
        try:
            # Escucha durante 10 segundos
            audio = recognizer.record(source, duration=10)
            print("Procesando el audio...")
            # Convierte el audio a texto usando Google Speech Recognition
            texto = recognizer.recognize_google(audio, language="es-ES")
            return texto
        except sr.UnknownValueError:
            print("No se entendió el audio.")
            return "No se entendió el audio."
        except sr.RequestError as e:
            print(f"Error con el servicio de reconocimiento: {e}")
            return "Error de servicio."

# myenv/Scripts/activate

# cd C:\Users\leonl\Downloads\trayectorias_robot\voz_tareas  
# python escuchar2.py
import speech_recognition as sr
import spacy
import time
import threading

# Cargar el modelo de spaCy
nlp = spacy.load("es_core_news_md")


# Definición de tareas y palabras clave para coincidencias
tareas = {
    "encender_luz": "Encendiendo la luz...",
    "apagar_luz": "Apagando la luz...",
    "reproducir_musica": "Reproduciendo música...",
    "detener_musica": "Deteniendo la música...",
    "seguir_mano": "Siguiendo la mano...",
    "detener_seguir_mano": "Deteniendo la tarea de seguir mano...",
    "seguir_objeto": "Siguiendo el objeto...",
    "detener_seguir_objeto": "Deteniendo la tarea de seguir objeto...",
    "monitorear_temperatura": "Monitoreando la temperatura...",
    "detener_monitorear_temperatura": "Deteniendo la tarea de monitoreo de temperatura..."
}




# Palabras clave de acciones (con sinónimos)
palabras_clave = {
    "encender_luz": {"verbo": ["encender", "prender"], "sustantivo": ["luz", "foco"]},
    "apagar_luz": {"verbo": ["apagar"], "sustantivo": ["luz", "foco"]},
    "reproducir_musica": {"verbo": ["reproducir", "tocar"], "sustantivo": ["música", "canción"]},
    "detener_musica": {"verbo": ["detener", "parar", "quita"], "sustantivo": ["música", "canción"]},
    "seguir_mano": {"verbo": ["seguir"], "sustantivo": ["mano"]},
    "detener_seguir_mano": {"verbo": ["detener", "parar", "dejar"], "sustantivo": ["seguir", "mano"]},
    "seguir_objeto": {"verbo": ["seguir"], "sustantivo": ["objeto"]},
    "detener_seguir_objeto": {"verbo": ["detener", "parar"], "sustantivo": ["seguir", "objeto"]},
    "monitorear_temperatura": {"verbo": ["monitorear", "controlar"], "sustantivo": ["temperatura", "calor"]},
    "detener_monitorear_temperatura": {"verbo": ["detener", "parar"], "sustantivo": ["monitorear", "temperatura"]}
}






# Lista de palabras que indican negación
palabras_negacion = ["evitar", "cancelar", "dejar", "parar", "no"]

# Lista de palabras que indican "alto" y sinónimos
palabras_alto = ["alto", "detente", "parar", "detener", "alto ahí"]

# Lista de palabras que indican "sí" y "no"
palabras_si = ["sí", "si", "claro", "por supuesto", "afirmativo"]
palabras_no = ["no", "negativo", "para nada", "nada"]

def procesar_comando(comando, palabras_clave , palabras_alto ):
    """Procesa el comando usando similitud semántica para identificar las tareas adecuadas."""
    global alto_por_comando
    doc = nlp(comando.lower())
    tarea_identificada = None
    es_negado = False
    similitud_maxima = 0.0  # Para rastrear la mayor similitud encontrada



    # Verificar si el comando contiene una solicitud de "alto" sin palabras clave de tarea
    contiene_alto = any(token.lemma_ in palabras_alto for token in doc)
    contiene_palabras_clave_tarea = any(
        token.lemma_ in palabras["verbo"] + palabras["sustantivo"]
        for tarea, palabras in palabras_clave.items()
        for token in doc
    )

    # Si solo se detecta "alto" sin palabras clave de tarea, retornar directamente "alto"
    if contiene_alto and not contiene_palabras_clave_tarea:
        print("Comando 'Alto' reconocido sin tareas adicionales. Activando bandera 'Alto'.")
        return "alto"

    # # Detección de negación (solo se llega aquí si no se activó el comando "alto")
    # es_negado = False
    # for token in doc:
    #     if token.lemma_ in palabras_negacion:
    #         es_negado = True
    #         break

    # # Si se detecta negación, se omite la ejecución de cualquier tarea
    # if es_negado:
    #     print("Se detectó negación. No se ejecutará ninguna tarea.")
    #     return "no_tarea"

    # Continuar con la lógica para otros comandos o tareas si es necesario
    print("Procesando otras tareas...")
    # Aquí puedes añadir la lógica adicional para otros comandos o tareas




    # Imprimir cada token con su parte del discurso y dependencia
    print("Análisis del comando:")
    for token in doc:
        print(f"{token.text} - {token.pos_} - {token.dep_}")

    # Procesamiento de cada token para encontrar la tarea con mayor similitud
    for token in doc:
        if token.pos_ == "VERB":
            for tarea, palabras in palabras_clave.items():
                # Obtener lemas de los verbos y sustantivos de las tareas
                verbos_tarea = [nlp(verbo)[0].lemma_ for verbo in palabras["verbo"]]
                sustantivos_tarea = [nlp(sust)[0].lemma_ for sust in palabras["sustantivo"]]

                # Comprobación de similitud para los verbos
                for verbo in verbos_tarea:
                    token_vec = nlp(token.lemma_)
                    verbo_vec = nlp(verbo)

                    if token_vec.has_vector and verbo_vec.has_vector:
                        similitud_verbo = token_vec.similarity(verbo_vec)
                        print(f"Similitud entre '{token.lemma_}' y '{verbo}': {similitud_verbo:.2f}")

                        # Se verifica si la similitud cumple el umbral y es mayor que la similitud máxima actual
                        if similitud_verbo >= 0.7 and similitud_verbo >= similitud_maxima:
                            for child in doc:
                                if child.pos_ == "NOUN":
                                    for sust in sustantivos_tarea:
                                        sust_token = nlp(sust)[0]

                                        if child.has_vector and sust_token.has_vector:
                                            similitud_sustantivo = child.similarity(sust_token)
                                            print(f"Similitud entre '{child.lemma_}' y '{sust}': {similitud_sustantivo:.2f}")
                                            
                                            # Si ambos cumplen el umbral y el sustantivo tiene una mejor similitud
                                            if similitud_sustantivo >= 0.75 and similitud_sustantivo >= similitud_maxima:
                                                # Actualizar la tarea y la similitud máxima
                                                tarea_identificada = tarea
                                                similitud_maxima = min(similitud_verbo, similitud_sustantivo)  # Más baja entre verbo y sustantivo

                                                # Prioridad de coincidencia al 100%
                                                if similitud_maxima == 1.0:
                                                    return tarea_identificada

    return tarea_identificada







def confirmar_tarea(respuesta, palabras_si, palabras_no):
    """Confirma con el usuario si desea ejecutar la tarea usando reconocimiento de voz."""
    
    if respuesta:
        # Procesar la respuesta
        respuesta_doc = nlp(respuesta.lower())
        for token in respuesta_doc:
            if token.lemma_ in palabras_no:
                return False
        for token in respuesta_doc:
            if token.lemma_ in palabras_si:
                return True
                
        print("Respuesta no reconocida. Por favor, repite.")
    else:
        print("No se entendió la respuesta.")
    
    return False  # Devuelve False si no se entiende la respuesta





if __name__ == "__main__":
    print(escuchar_comando())