from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
import matplotlib.pyplot as plt
import numpy as np
import os
from sympy import Matrix

# Inicialización del proyecto usando Flask
app = Flask(__name__)

# Diccionario de traducciones
translations = {
    # Palabra claves basicas usadas en ingles para la interfaz
    'en': {
        'Encrypt': 'Encrypt',
        'Decrypt': 'Decrypt',
        'Options': 'Options',
        'About Me': 'About Me',
        'Dark Mode:': 'Dark Mode:',
        'Volume:': 'Volume:',
        'Language:': 'Language:',
        'Back': 'Back',
        'ENCRYPT TEXT':'ENCRYPT TEXT',
        'DECRYPT TEXT':'DECRYPT TEXT',
        'Tool for encoding text with different systems':'Tool for encoding text with different systems',
        'Insert the text here':'Insert the text here',
        'Project for cryptography':'Project for cryptography'
    },
    # Palabra claves basicas usadas en español para la interfaz
    'es': {
        'Encrypt': 'Cifrar',
        'Decrypt': 'Descifrar',
        'Options': 'Opciones',
        'About Me': 'Acerca de mí',
        'Dark Mode:': 'Modo oscuro:',
        'Volume:': 'Volumen:',
        'Language:': 'Idioma:',
        'Back': 'Volver',
        'ENCRYPT TEXT':'ENCRIPTAR TEXTO',
        'DECRYPT TEXT':'DESCIFRAR TEXTO',
        'Tool for encoding text with different systems':'Herramienta para codificar texto con diferentes sistemas',
        'Insert the text here':'Insertar el texto aquí',
        'Project for cryptography':'Proyecto para criptografía'
    },
    # Palabra claves basicas usadas en portugues para la interfaz
    'pt': {
        'Encrypt': 'Criptografar',
        'Decrypt': 'Descriptografar',
        'Options': 'Opções',
        'About Me': 'Sobre mim',
        'Dark Mode:': 'Modo escuro:',
        'Volume:': 'Volume:',
        'Language:': 'Idioma:',
        'Back': 'Voltar',
        'ENCRYPT TEXT':'CRIPTOGRAFAR TEXTO',
        'DECRYPT TEXT':'DESCRIPTOGRAFAR TEXTO',
        'Tool for encoding text with different systems':'Ferramenta para codificar texto com diferentes sistemas',
        'Insert the text here':'Insira o texto aqui',
        'Project for cryptography':'Projeto para criptografia'
    }
}

def translate_text(text, lang):
    """
        Traduce un texto al idioma especificado si la traducción está disponible en el diccionario 'translations'.

        Args:
        text (str): El texto que se desea traducir.
        lang (str): El código del idioma al que se desea traducir el texto (por ejemplo, 'en' para inglés, 'es' para español).

        Returns:
        str: La traducción del texto si se encuentra disponible; de lo contrario, devuelve el texto original.
    """
    if lang in translations and text in translations[lang]:
        return translations[lang][text]
    return text

@app.route('/')
def index():
    """
    Maneja la ruta principal ('/') de la aplicación web.

    Obtiene las preferencias de modo oscuro y de idioma del usuario a través de cookies y
    renderiza la plantilla 'index.html' con estas preferencias.

    Cookies:
        - 'dark-mode': Almacena si el modo oscuro está activado ('1') o desactivado ('0').
        - 'locale': Almacena el idioma preferido del usuario (por ejemplo, 'es' para español).

    Plantilla renderizada:
        - index.html: La plantilla HTML que se mostrará al usuario.

    Contexto de la plantilla:
        - dark_mode (bool): Indica si el modo oscuro está activado o desactivado.
        - translate (function): La función `translate_text` para traducir textos dentro de la plantilla.
        - lang (str): El idioma seleccionado por el usuario (por defecto 'es').

    Returns:
        str: El HTML renderizado de la plantilla 'index.html'.
    """
    dark_mode = request.cookies.get('dark-mode', '0') == '1'
    lang = request.cookies.get('locale', 'es')
    return render_template('index.html', dark_mode=dark_mode, translate=translate_text, lang=lang)

@app.route('/encrypt', methods=['GET', 'POST'])
def encrypt():
    """
    Maneja la ruta '/encrypt' para encriptar mensajes usando diferentes algoritmos.

    Si la solicitud es 'GET', renderiza la página con el formulario de encriptación.
    Si la solicitud es 'POST', procesa los datos del formulario y ejecuta el algoritmo de encriptación seleccionado.

    Cookies:
        - 'dark-mode': Almacena si el modo oscuro está activado ('1') o desactivado ('0').
        - 'locale': Almacena el idioma preferido del usuario (por defecto 'es' para español).

    Métodos de solicitud:
        - GET: Renderiza la plantilla 'encrypt.html'.
        - POST: Procesa los datos del formulario y ejecuta el algoritmo de encriptación.

    Formularios de datos (POST):
        - 'message' (str): El mensaje que se desea encriptar.
        - 'algorithm' (str): El algoritmo de encriptación seleccionado ('cesar', 'monoalfabetico', 'playfair', 'hill').
        - 'alphabet' (str): (Opcional) El alfabeto utilizado para el cifrado César.
        - 'key' (int): (Opcional) La clave de cifrado para el algoritmo César.
        - 'key_playfair' (str): (Opcional) La clave utilizada para el cifrado Playfair.
        - 'key_matrix_hill' (str): (Opcional) La clave en forma de matriz para el cifrado Hill.

    Retorno (POST):
        - JSON: Un diccionario JSON con las siguientes claves:
            - 'message': El mensaje original enviado.
            - 'algorithm': El algoritmo utilizado para encriptar el mensaje.
            - 'result': El resultado del mensaje encriptado o un mensaje de error si el algoritmo no está soportado.

    Renderización (GET):
        - encrypt.html: La plantilla HTML con la interfaz para ingresar datos de encriptación.

    Returns:
        - Si la solicitud es GET: El HTML renderizado de la plantilla 'encrypt.html'.
        - Si la solicitud es POST: Un diccionario JSON con el mensaje original, el algoritmo y el resultado de la encriptación.
    """
    dark_mode = request.cookies.get('dark-mode', '0') == '1'
    lang = request.cookies.get('locale', 'es')
    
    if request.method == 'POST':
        message = request.form['message']
        algorithm = request.form['algorithm']
        
        if algorithm == 'cesar':
            alphabet = request.form['alphabet']
            key = int(request.form['key'])
            result = encrypt_cesar(message, alphabet, key)
        elif algorithm == 'monoalfabetico':
            result = encrypt_monoalfabetico(message)
        elif algorithm == 'playfair':
            key_plane = request.form['key_playfair']
            print ("key_plane: "+ key_plane)
            result = encrypt_playfair(message, key_plane)  # Se pasa como argumento
        elif algorithm == 'hill':
            key_plane = request.form['key_matrix_hill']
            key_matrix = string_to_matrix(key_plane)
            result = encrypt_hill(message, key_matrix)
        else:
            result = 'Algoritmo no soportado'
        return jsonify({'message': message, 'algorithm': algorithm, 'result': result})
    return render_template('encrypt.html', dark_mode=dark_mode, translate=translate_text, lang=lang)

@app.route('/decrypt', methods=['GET', 'POST'])
def decrypt():
    """
    Maneja la ruta '/decrypt' para desencriptar mensajes usando diferentes algoritmos.

    Si la solicitud es 'GET', renderiza la página con el formulario de desencriptación.
    Si la solicitud es 'POST', procesa los datos del formulario y ejecuta el algoritmo de desencriptación seleccionado.

    Cookies:
        - 'dark-mode': Almacena si el modo oscuro está activado ('1') o desactivado ('0').
        - 'locale': Almacena el idioma preferido del usuario (por defecto 'es' para español).

    Métodos de solicitud:
        - GET: Renderiza la plantilla 'decrypt.html'.
        - POST: Procesa los datos del formulario y ejecuta el algoritmo de desencriptación.

    Formularios de datos (POST):
        - 'encrypted_message' (str): El mensaje que se desea desencriptar.
        - 'algorithm' (str): El algoritmo de desencriptación seleccionado ('cesar', 'monoalfabetico', 'playfair', 'hill').
        - 'alphabet' (str): (Opcional) El alfabeto utilizado para el descifrado César.
        - 'key' (int): (Cesar) La clave de descifrado para el algoritmo César.
        - 'key_playfair' (str): (PlayFair) La clave utilizada para el descifrado Playfair.
        - 'key_matrix_hill' (str): (Hill) La clave en forma de matriz para el descifrado Hill.

    Retorno (POST):
        - JSON: Un diccionario JSON con las siguientes claves:
            - 'encrypted_message': El mensaje encriptado enviado.
            - 'algorithm': El algoritmo utilizado para desencriptar el mensaje.
            - 'result': El resultado del mensaje desencriptado o un mensaje de error si el algoritmo no está soportado.

    Renderización (GET):
        - decrypt.html: La plantilla HTML con la interfaz para ingresar datos de desencriptación.

    Returns:
        - Si la solicitud es GET: El HTML renderizado de la plantilla 'decrypt.html'.
        - Si la solicitud es POST: Un diccionario JSON con el mensaje encriptado, el algoritmo y el resultado de la desencriptación.
    """
    dark_mode = request.cookies.get('dark-mode', '0') == '1'
    lang = request.cookies.get('locale', 'es')
    
    if request.method == 'POST':
        encrypted_message = request.form['encrypted_message']
        algorithm = request.form['algorithm']
        
        if algorithm == 'cesar':
            alphabet = request.form['alphabet']
            key = int(request.form['key'])
            result = decrypt_cesar(encrypted_message, alphabet, key)
        elif algorithm == 'monoalfabetico':
            result = decrypt_monoalfabetico(encrypted_message)
        elif algorithm == 'playfair':
            key = request.form['key_playfair']
            result = decrypt_playfair(encrypted_message, key)
        elif algorithm == 'hill':
            key_plane = request.form['key_matrix_hill']
            key_matrix = string_to_matrix(key_plane)
            result = decrypt_hill(encrypted_message, key_matrix)
        else:
            result = 'Algoritmo no soportado'
        
        return jsonify({'encrypted_message': encrypted_message, 'algorithm': algorithm, 'result': result})
    
    return render_template('decrypt.html', dark_mode=dark_mode, translate=translate_text, lang=lang)


@app.route('/options')
def options():
    """
    Maneja la ruta '/options' para mostrar la página de configuración de la aplicación.

    Esta función recupera las preferencias de usuario almacenadas en cookies, como el modo oscuro, 
    el idioma y el nivel de volumen, y las pasa a la plantilla 'options.html' para su visualización 
    y ajuste por parte del usuario.

    Cookies:
        - 'dark-mode': Almacena si el modo oscuro está activado ('1') o desactivado ('0').
        - 'locale': Almacena el idioma preferido del usuario (por defecto 'es' para español).
        - 'volume': Almacena el nivel de volumen para la música de fondo (valor entre 0.0 y 1.0).

    Renderización:
        - options.html: La plantilla HTML que contiene las opciones de configuración de la aplicación.

    Contexto pasado a la plantilla:
        - dark_mode (bool): Indica si el modo oscuro está activado o no.
        - lang (str): El idioma seleccionado para la interfaz de la aplicación.
        - translate (func): La función de traducción para adaptar el contenido a diferentes idiomas.
        - volume (float): El nivel de volumen de la música de fondo.

    Returns:
        - El HTML renderizado de la plantilla 'options.html' con las preferencias del usuario.
    """
    dark_mode = request.cookies.get('dark-mode', '0') == '1'
    lang = request.cookies.get('locale', 'es')
    volume = request.cookies.get('volume', '0') 
    return render_template('options.html', dark_mode=dark_mode, translate=translate_text, lang=lang, volume=float(volume))

@app.route('/about')
def about():
    """
    Maneja la ruta '/about' para mostrar la página de información de la aplicación.

    Esta función recupera las preferencias de usuario almacenadas en cookies, como el modo oscuro 
    y el idioma, y las pasa a la plantilla 'about.html' para personalizar la presentación de la 
    página de información.

    Cookies:
        - 'dark-mode': Almacena si el modo oscuro está activado ('1') o desactivado ('0').
        - 'locale': Almacena el idioma preferido del usuario (por defecto 'es' para español).

    Renderización:
        - about.html: La plantilla HTML que contiene la información sobre la aplicación.

    Contexto pasado a la plantilla:
        - dark_mode (bool): Indica si el modo oscuro está activado o no.
        - lang (str): El idioma seleccionado para la interfaz de la aplicación.
        - translate (func): La función de traducción para adaptar el contenido a diferentes idiomas.

    Returns:
        - El HTML renderizado de la plantilla 'about.html' con las preferencias del usuario.
    """
    dark_mode = request.cookies.get('dark-mode', '0') == '1'
    lang = request.cookies.get('locale', 'es')
    return render_template('about.html', dark_mode=dark_mode, translate=translate_text, lang=lang)

@app.route('/set_dark_mode/<int:status>')
def set_dark_mode(status):
    """
    Actualiza el estado del modo oscuro en las preferencias del usuario mediante cookies.

    Esta función recibe un parámetro `status` que determina si el modo oscuro debe ser 
    activado (`1`) o desactivado (`0`). El estado es almacenado en la cookie 'dark-mode'. 
    Luego, se devuelve una respuesta en formato JSON confirmando que la operación fue 
    exitosa.

    Args:
        status (int): Estado del modo oscuro, donde `1` lo activa y `0` lo desactiva.

    Cookies:
        - 'dark-mode': Se establece a '1' si el modo oscuro está activado o a '0' si está desactivado.

    Returns:
        - Una respuesta HTTP con un JSON que indica el éxito de la operación.
    """
    resp = make_response({'status': 'success'})
    resp.set_cookie('dark-mode', str(status))
    return resp

@app.route('/set_language/<language>')
def set_language(language):
    """
    Actualiza la preferencia de idioma del usuario mediante cookies y redirige a la página anterior.

    Esta función recibe un parámetro `language` que determina el idioma seleccionado por el usuario.
    El idioma se almacena en la cookie 'locale'. Luego, el usuario es redirigido a la página desde 
    la cual hizo la solicitud, manteniendo así su flujo de navegación.

    Args:
        language (str): Código del idioma seleccionado (por ejemplo, 'es' para español, 'en' para inglés).

    Cookies:
        - 'locale': Se establece con el código del idioma seleccionado.

    Returns:
        - Una redirección HTTP a la página anterior del usuario.
    """
    resp = redirect(request.referrer)
    resp.set_cookie('locale', language)
    return resp

@app.route('/set_volume/<float:volume>')
def set_volume(volume):
    """
    Actualiza la preferencia de volumen del usuario mediante cookies.

    Esta función recibe un parámetro `volume` que determina el nivel de volumen seleccionado 
    por el usuario. El nivel de volumen se almacena en la cookie 'volume'. 

    Args:
        volume (float): Nivel de volumen seleccionado, expresado como un número flotante.

    Cookies:
        - 'volume': Se establece con el valor del nivel de volumen seleccionado.

    Returns:
        - Una respuesta JSON que indica el éxito de la operación ('status': 'success').
    """
    resp = make_response({'status': 'success'})
    resp.set_cookie('volume', str(volume))
    return resp

""" Funciones /// Functions /// Funções /// Funciones /// Functions /// Funções """

# Función para la encriptación utilizando el método Caesar
def encrypt_cesar(message, alphabet, key):
    """
    Cifra un mensaje utilizando el cifrado César.

    Este algoritmo desplaza cada letra del mensaje original un número fijo de posiciones, 
    determinado por la clave `key`, dentro del alfabeto proporcionado. Si un carácter no está en el 
    alfabeto, se deja sin cambios.

    Args:
        message (str): El mensaje a cifrar.
        alphabet (str): El alfabeto utilizado para el cifrado. Debe ser una cadena de caracteres 
                        donde cada carácter es único.
        key (int): El número de posiciones a desplazar cada carácter en el alfabeto.

    Returns:
        str: El mensaje cifrado donde cada carácter ha sido desplazado según la clave `key`.

    Ejemplo:
        Si el mensaje es "HELLO", el alfabeto es "ABCDEFGHIJKLMNOPQRSTUVWXYZ", y la clave es 3,
        el mensaje cifrado será "KHOOR".
    """
    encrypted_message = ''
    for char in message:
        if char in alphabet:
            # Find the current position of the character # Encuentra la posición actual del carácter
            original_index = alphabet.index(char)
            # Calculate the new position with the key # Calcula la nueva posición con la clave
            new_index = (original_index + key) % len(alphabet)
            # Append the encrypted character to the result # Añade el carácter cifrado al resultado
            encrypted_message += alphabet[new_index]
        else:
            # If the character is not in the alphabet, keep it unchanged
            # Si el carácter no está en el alfabeto, se mantiene sin cambios
            encrypted_message += char
    return encrypted_message

# Función para la desencriptación utilizando el método Caesar
def decrypt_cesar(message, alphabet, key):
    """
    Descifra un mensaje cifrado con el cifrado César.

    Este algoritmo desplaza cada letra del mensaje cifrado en la dirección opuesta al cifrado, 
    utilizando el número fijo de posiciones determinado por la clave `key`, dentro del alfabeto proporcionado. 
    Si un carácter no está en el alfabeto, se deja sin cambios.

    Args:
        message (str): El mensaje cifrado que se desea descifrar.
        alphabet (str): El alfabeto utilizado para el cifrado. Debe ser una cadena de caracteres 
                        donde cada carácter es único.
        key (int): El número de posiciones por el cual se desplazó cada carácter en el alfabeto durante el cifrado.

    Returns:
        str: El mensaje descifrado donde cada carácter ha sido desplazado hacia atrás según la clave `key`.
    """
    decrypted_message = ''
    for char in message:
        if char in alphabet:
            # Find the current position of the character # Encuentra la posición actual del carácter
            encrypted_index = alphabet.index(char)
            # Calculate the original position with the key # Calcula la posición original con la clave, desplazando hacia atrás
            original_index = (encrypted_index - key) % len(alphabet)
            # Append the decrypted character to the result # Añade el carácter descifrado al resultado
            decrypted_message += alphabet[original_index]
        else:
            # If the character is not in the alphabet, keep it unchanged # Si el carácter no está en el alfabeto, se mantiene sin cambios
            decrypted_message += char
    return decrypted_message

# Función para la encriptación utilizando el método monoalfabetico (con la variable de porcentaje de frecuencia en el lenguaje español)
def encrypt_monoalfabetico(message):
    """
    Cifra un mensaje usando un cifrado monoalfabético basado en un mapa de sustitución fijo.

    En este cifrado, cada carácter del mensaje se reemplaza por otro carácter según un mapa de sustitución predefinido. 
    El mapa se basa en la frecuencia típica de caracteres en español, y el cifrado es sensible al caso de las letras. 
    Si un carácter no está en el mapa de sustitución, se mantiene sin cambios.

    Args:
        message (str): El mensaje que se desea cifrar.

    Returns:
        str: El mensaje cifrado, donde cada carácter ha sido reemplazado según el mapa de sustitución.
    """
    # Mapa de sustitución fijo basado en la frecuencia típica de caracteres en español
    substitution_map = {
        'a': 'o', 'b': 'p', 'c': 'q', 'd': 'r', 'e': 's', 'f': 't', 'g': 'u', 'h': 'v',
        'i': 'w', 'j': 'x', 'k': 'y', 'l': 'z', 'm': 'a', 'n': 'b', 'ñ': 'c', 'o': 'd',
        'p': 'e', 'q': 'f', 'r': 'g', 's': 'h', 't': 'i', 'u': 'j', 'v': 'k', 'w': 'l',
        'x': 'm', 'y': 'n', 'z': 'ñ'
    }
    
    encrypted_message = ''
    for char in message:
        if char.lower() in substitution_map:
            encrypted_char = substitution_map[char.lower()]
            # Mantener el caso original del carácter
            if char.isupper():
                encrypted_message += encrypted_char.upper()
            else:
                encrypted_message += encrypted_char
        else:
            # Si el carácter no está en el mapa, se mantiene sin cambios
            encrypted_message += char
    return encrypted_message

# Función para la desencriptación utilizando el método monoalfabetico (con la variable de porcentaje de frecuencia en el lenguaje español)
def decrypt_monoalfabetico(encrypted_message):
    """
    Descifra un mensaje cifrado usando un cifrado monoalfabético basado en un mapa de sustitución fijo.

    En este cifrado, cada carácter cifrado se reemplaza por el carácter original utilizando un mapa de sustitución inverso.
    La función es sensible al caso de las letras. Si un carácter no está en el mapa de sustitución, se mantiene sin cambios.

    Args:
        encrypted_message (str): El mensaje cifrado que se desea descifrar.

    Returns:
        str: El mensaje descifrado, donde cada carácter ha sido reemplazado según el mapa de sustitución inverso.
    """
    # Mapa inverso de sustitución
    reverse_substitution_map = {v: k for k, v in {
        'a': 'o', 'b': 'p', 'c': 'q', 'd': 'r', 'e': 's', 'f': 't', 'g': 'u', 'h': 'v',
        'i': 'w', 'j': 'x', 'k': 'y', 'l': 'z', 'm': 'a', 'n': 'b', 'ñ': 'c', 'o': 'd',
        'p': 'e', 'q': 'f', 'r': 'g', 's': 'h', 't': 'i', 'u': 'j', 'v': 'k', 'w': 'l',
        'x': 'm', 'y': 'n', 'z': 'ñ'
    }.items()}

    decrypted_message = ''
    for char in encrypted_message:
        if char.lower() in reverse_substitution_map:
            decrypted_char = reverse_substitution_map[char.lower()]
            # Mantener el caso original del carácter
            if char.isupper():
                decrypted_message += decrypted_char.upper()
            else:
                decrypted_message += decrypted_char
        else:
            # Si el carácter no está en el mapa, se mantiene sin cambios
            decrypted_message += char

    return decrypted_message

# Función para la encriptación utilizando el método PlayFair
def encrypt_playfair(message, key):
    """
    Cifra un mensaje utilizando el cifrado Playfair con una clave dada.

    Este método de cifrado trabaja en pares de letras, utilizando una matriz de 5x5 construida a partir de la clave.
    Si un par de letras es igual o si el mensaje tiene longitud impar, se inserta 'X' como relleno.

    Args:
        message (str): El mensaje que se desea cifrar.
        key (str): La clave utilizada para construir la matriz de cifrado.

    Returns:
        str: El mensaje cifrado.
    """
    # Convertir mensaje y clave a mayúsculas y limpiar
    message = message.upper().replace("J", "I").replace("Ñ", "N")
    message = ''.join(filter(str.isalpha, message))  # Filtrar solo letras

    key = key.upper().replace(" ", "").replace("Ñ", "N")
    key = ''.join(filter(str.isalpha, key))  # Filtrar solo letras

    # Validar que la clave solo contenga letras
    if not key.isalpha():
        raise ValueError("La clave solo debe contener letras y no puede incluir caracteres especiales o espacios.")

    # Eliminar caracteres duplicados de la clave
    key = ''.join(sorted(set(key), key=lambda x: key.index(x)))

    # Crear la matriz 5x5 usando la clave
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"  # Se excluye la 'J' para el alfabeto Playfair
    matrix = []
    for char in key:
        if char in alphabet:
            matrix.append(char)
            alphabet = alphabet.replace(char, "")  # Eliminar la letra del alfabeto
    matrix.extend(alphabet)  # Añadir el resto del alfabeto

    # Convertir la lista en una matriz de 5x5
    matrix_5x5 = [matrix[i:i + 5] for i in range(0, 25, 5)]

    # Mostrar la matriz para verificarla
    print("Matriz 5x5:")
    for row in matrix_5x5:
        print(row)

    # Dividir el mensaje en pares de letras
    def prepare_message(message):
        pairs = []
        i = 0
        while i < len(message):
            pair = message[i]
            if i + 1 < len(message):
                if message[i] != message[i + 1]:
                    pair += message[i + 1]
                    i += 2
                else:
                    pair += "X"  # Insertar 'X' entre letras iguales
                    i += 1
            else:
                pair += "X"  # Agregar 'X' si el mensaje tiene longitud impar
                i += 1
            pairs.append(pair)
        return pairs

    pairs = prepare_message(message)
    print("Pares generados:", pairs)  # Imprimir los pares generados

    # Función para obtener la posición de una letra en la matriz
    def get_position(char):
        for row in range(5):
            if char in matrix_5x5[row]:
                col = matrix_5x5[row].index(char)
                return row, col
        return None

    # Cifrar cada par de letras
    encrypted_message = []
    for pair in pairs:
        row1, col1 = get_position(pair[0])
        row2, col2 = get_position(pair[1])

        # Mostrar las posiciones encontradas
        print(f"Posiciones para {pair}: ({row1}, {col1}), ({row2}, {col2})")

        # Validar que ambas letras existen en la matriz
        if row1 is None or row2 is None:
            raise ValueError(f"Error al encontrar las posiciones de los caracteres '{pair[0]}' o '{pair[1]}' en la matriz Playfair.")

        if row1 == row2:  # Misma fila
            encrypted_message.append(matrix_5x5[row1][(col1 + 1) % 5])
            encrypted_message.append(matrix_5x5[row2][(col2 + 1) % 5])
        elif col1 == col2:  # Misma columna
            encrypted_message.append(matrix_5x5[(row1 + 1) % 5][col1])
            encrypted_message.append(matrix_5x5[(row2 + 1) % 5][col2])
        else:  # Rectángulo
            encrypted_message.append(matrix_5x5[row1][col2])
            encrypted_message.append(matrix_5x5[row2][col1])

    return ''.join(encrypted_message)

# Función para la desencriptación utilizando el método PlayFair
def decrypt_playfair(ciphertext, key):
    """
    Esta función descifra un mensaje cifrado utilizando el cifrado Playfair y una clave dada.
    
    El cifrado Playfair es un método de encriptación que opera sobre pares de letras. 
    La clave se utiliza para crear una matriz de 5x5 que contiene todas las letras del alfabeto, 
    excluyendo la 'J'. Luego, el texto cifrado se divide en pares de letras que se descifran 
    utilizando reglas específicas según su posición en la matriz. 
    La función devuelve el mensaje original descifrado.
    
    Args:
    ciphertext: El mensaje cifrado que debe ser descifrado.
    key: La clave utilizada para construir la matriz de cifrado.

    Returns:
    El mensaje original descifrado.
    """
    # Validar y limpiar el texto cifrado
    # Convertir el texto cifrado a mayúsculas, eliminar espacios y reemplazar 'Ñ' por 'N'
    ciphertext = ciphertext.upper().replace(" ", "").replace("Ñ", "N")
    # Filtrar solo las letras del texto cifrado
    ciphertext = ''.join(filter(str.isalpha, ciphertext))

    # Validar y limpiar la clave
    # Convertir la clave a mayúsculas, eliminar espacios y reemplazar 'Ñ' por 'N'
    key = key.upper().replace(" ", "").replace("Ñ", "N")
    # Filtrar solo las letras de la clave
    key = ''.join(filter(str.isalpha, key))

    # Validar que la clave solo contenga letras
    if not key.isalpha():
        raise ValueError("La clave solo debe contener letras y no puede incluir caracteres especiales o espacios.")

    # Eliminar caracteres duplicados de la clave
    key = ''.join(sorted(set(key), key=lambda x: key.index(x)))

    # Crear la matriz 5x5 usando la clave
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ" # Se excluye la 'J' para el alfabeto Playfair
    matrix = []
    for char in key:
        if char in alphabet:
            matrix.append(char)
            alphabet = alphabet.replace(char, "") # Eliminar la letra del alfabeto
    # Añadir el resto del alfabeto a la matriz
    matrix.extend(alphabet)
    
    # Convertir la lista en una matriz de 5x5
    matrix_5x5 = [matrix[i:i + 5] for i in range(0, 25, 5)]

    # Función para obtener la posición de una letra en la matriz
    def get_position(char):
        for row in range(5):
            if char in matrix_5x5[row]:
                col = matrix_5x5[row].index(char)
                return row, col
        return None

    # Dividir el texto cifrado en pares de letras
    def split_into_pairs(ciphertext):
        return [ciphertext[i:i + 2] for i in range(0, len(ciphertext), 2)]

    # Obtener los pares de letras del texto cifrado
    pairs = split_into_pairs(ciphertext)

    # Descifrar cada par de letras
    decrypted_message = []
    for pair in pairs:
        # Obtener las posiciones de cada letra en la matriz
        row1, col1 = get_position(pair[0])
        row2, col2 = get_position(pair[1])

        # Si las letras están en la misma fila
        if row1 == row2:
            decrypted_message.append(matrix_5x5[row1][(col1 - 1) % 5])
            decrypted_message.append(matrix_5x5[row2][(col2 - 1) % 5])
        # Si las letras están en la misma columna
        elif col1 == col2:
            decrypted_message.append(matrix_5x5[(row1 - 1) % 5][col1])
            decrypted_message.append(matrix_5x5[(row2 - 1) % 5][col2])
        # Si las letras forman un rectángulo (distintas fila y columna)
        else:
            decrypted_message.append(matrix_5x5[row1][col2])
            decrypted_message.append(matrix_5x5[row2][col1])
    # Unir las letras descifradas en un solo mensaje
    return ''.join(decrypted_message)

# Función para la encriptación utilizando el método Hill
def encrypt_hill(plaintext, key_matrix):
    """
    Esta función cifra un mensaje utilizando el cifrado de Hill, que es un tipo de cifrado de bloques 
    basado en álgebra lineal. Usa una matriz clave para transformar bloques de letras del texto encriptado.

    Args:
    plaintext: El mensaje que se desea cifrar.
    key_matrix: La matriz clave utilizada para cifrar el mensaje, debe ser una matriz cuadrada.

    Returns:
    El mensaje cifrado como una cadena de texto.
    """

    # Convertir el mensaje a mayúsculas y remover espacios
    plaintext = plaintext.upper().replace(" ", "")
    
    # Verificar que la clave sea una matriz cuadrada y que el mensaje sea válido
    key_size = len(key_matrix)
    if any(len(row) != key_size for row in key_matrix):
        raise ValueError("La clave debe ser una matriz cuadrada.")

    # Validar que la longitud del texto plano sea múltiplo del tamaño de la matriz
    if len(plaintext) % key_size != 0:
        # Rellenar con 'X' para completar el bloque
        padding = key_size - (len(plaintext) % key_size)
        plaintext += 'X' * padding
    
    # Convertir el texto a números (A=0, B=1, ..., Z=25)
    def char_to_num(char):
        return ord(char) - ord('A')

    def num_to_char(num):
        return chr((num % 26) + ord('A'))

    # Dividir el texto en bloques de acuerdo al tamaño de la matriz
    blocks = [plaintext[i:i+key_size] for i in range(0, len(plaintext), key_size)]

    # Convertir cada bloque en un vector y aplicar la matriz clave
    encrypted_message = []
    for block in blocks:
        # Convertir el bloque en un vector de números
        block_vector = np.array([char_to_num(char) for char in block]).reshape(-1, 1)
        # Multiplicar la matriz clave por el vector del bloque y aplicar módulo 26
        encrypted_vector = np.dot(key_matrix, block_vector) % 26
        # Convertir el vector cifrado de vuelta a letras y añadirlo al mensaje cifrado
        encrypted_message.extend([num_to_char(num) for num in encrypted_vector.flatten()])
    # Unir las letras cifradas en un solo mensaje cifrado
    return ''.join(encrypted_message)

# Función para devolver la matriz inversa modular
def mod_inverse(matrix, mod):
    """
    Esta función calcula la inversa modular de una matriz cuadrada, utilizando el determinante
    de la matriz y su inversa, todo bajo un módulo específico.

    Parámetros:
    matrix: La matriz cuadrada a la que se le desea calcular la inversa modular.
    mod: El módulo bajo el cual se realizará el cálculo.

    Retorna:
    La inversa modular de la matriz en el módulo especificado.
    """

    # Calcular el determinante de la matriz y redondearlo al entero más cercano
    det = int(round(np.linalg.det(matrix)))  # Determinante de la matriz
    # Calcular la inversa del determinante en el módulo especificado
    det_inv = pow(det, -1, mod)  # Inversa modular del determinante bajo mod
    # Calcular la inversa de la matriz, multiplicarla por el determinante y luego por su inversa modular
    matrix_mod_inv = det_inv * np.round(det * np.linalg.inv(matrix)).astype(int) % mod
    # Retornar la matriz inversa modular
    return matrix_mod_inv


"""-------------------------------------------------------------------------------------------------"""
# Función para la desencriptación utilizando el método Hill
def decrypt_hill(ciphertext, key_matrix):
    """
    Esta función descifra un mensaje utilizando el cifrado de Hill.
    El proceso inverso al cifrado utiliza la inversa modular de la matriz clave.

    Args:
    ciphertext: El mensaje cifrado a descifrar (debe estar en letras mayúsculas y sin espacios).
    key_matrix: La matriz clave utilizada para cifrar el mensaje.

    Returns:
    El mensaje descifrado en texto plano.
    """

    # Convertir el mensaje cifrado a mayúsculas y remover espacios
    ciphertext = ciphertext.upper().replace(" ", "")

    # Verificar que la clave sea una matriz cuadrada
    key_size = len(key_matrix)
    if any(len(row) != key_size for row in key_matrix):
        raise ValueError("La clave debe ser una matriz cuadrada.")

    # Calcular la inversa modular de la matriz clave
    key_matrix_inv = mod_inverse(key_matrix, 26)

    # Convertir el texto cifrado a números (A=0, B=1, ..., Z=25)
    def char_to_num(char):
        return ord(char) - ord('A')

    def num_to_char(num):
        return chr((num % 26) + ord('A'))

    # Dividir el texto cifrado en bloques de acuerdo al tamaño de la matriz
    blocks = [ciphertext[i:i+key_size] for i in range(0, len(ciphertext), key_size)]

    # Convertir cada bloque en un vector y aplicar la matriz inversa clave
    decrypted_message = []
    for block in blocks:
        # Convertir el bloque de texto a un vector numérico
        block_vector = np.array([char_to_num(char) for char in block]).reshape(-1, 1)
        # Multiplicar el vector por la matriz inversa y aplicar módulo 26
        decrypted_vector = np.dot(key_matrix_inv, block_vector) % 26
        # Convertir el vector numérico de vuelta a texto
        decrypted_message.extend([num_to_char(num) for num in decrypted_vector.flatten()])
    # Retornar el mensaje descifrado como una cadena de texto
    return ''.join(decrypted_message)

def string_to_matrix(matrix_string):
    """
    Esta función convierte una cadena de texto en una matriz cuadrada de números enteros.
    
    Parámetros:
    matrix_string: Una cadena de texto que representa la matriz, donde los elementos están separados por comas.

    Retorna:
    Una matriz 2D (array de NumPy) de números enteros.
    """

    # Limpiar la cadena eliminando espacios en blanco innecesarios
    matrix_string = matrix_string.strip()

    # Convertir la cadena en una lista de enteros, ignorando elementos vacíos
    # Se utiliza 'filter(None, ...)' para evitar incluir elementos vacíos si hay múltiples comas seguidas
    matrix_list = list(map(int, filter(None, matrix_string.split(','))))

    # Calcular el tamaño de la matriz (debe ser cuadrada)
    # El tamaño es la raíz cuadrada del número total de elementos
    size = int(len(matrix_list) ** 0.5)

    # Verificar si la longitud de la lista es un número cuadrado perfecto
    # Esto asegura que la matriz sea cuadrada
    if size * size != len(matrix_list):
        raise ValueError("La clave debe formar una matriz cuadrada.")

    # Convertir la lista de enteros en una matriz 2D de NumPy con forma (size, size)
    matrix = np.array(matrix_list).reshape(size, size)
    return matrix

if __name__ == '__main__':
    app.run(debug=True)