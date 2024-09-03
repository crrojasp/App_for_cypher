from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
import matplotlib.pyplot as plt
from ecdsa import SigningKey, SECP256k1
import numpy as np
import os
from sympy import Matrix


app = Flask(__name__)

# Diccionario de traducciones
translations = {
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
    if lang in translations and text in translations[lang]:
        return translations[lang][text]
    return text

@app.route('/')
def index():
    dark_mode = request.cookies.get('dark-mode', '0') == '1'
    lang = request.cookies.get('locale', 'es')
    return render_template('index.html', dark_mode=dark_mode, translate=translate_text, lang=lang)

@app.route('/encrypt', methods=['GET', 'POST'])
def encrypt():
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

        # Aquí podrías decidir qué hacer con el resultado, por ejemplo:
        # renderizar otra plantilla o redirigir a otra página.
        # Por ahora, devolveremos un JSON como ejemplo.
        return jsonify({'message': message, 'algorithm': algorithm, 'result': result})
    
    return render_template('encrypt.html', dark_mode=dark_mode, translate=translate_text, lang=lang)

@app.route('/decrypt', methods=['GET', 'POST'])
def decrypt():
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
    dark_mode = request.cookies.get('dark-mode', '0') == '1'
    lang = request.cookies.get('locale', 'es')
    volume = request.cookies.get('volume', '0') 
    return render_template('options.html', dark_mode=dark_mode, translate=translate_text, lang=lang, volume=float(volume))

@app.route('/about')
def about():
    dark_mode = request.cookies.get('dark-mode', '0') == '1'
    lang = request.cookies.get('locale', 'es')
    return render_template('about.html', dark_mode=dark_mode, translate=translate_text, lang=lang)

@app.route('/set_dark_mode/<int:status>')
def set_dark_mode(status):
    resp = make_response({'status': 'success'})
    resp.set_cookie('dark-mode', str(status))
    return resp

@app.route('/set_language/<language>')
def set_language(language):
    resp = redirect(request.referrer)
    resp.set_cookie('locale', language)
    return resp

@app.route('/set_volume/<float:volume>')
def set_volume(volume):
    resp = make_response({'status': 'success'})
    resp.set_cookie('volume', str(volume))
    return resp


# Funciones de cifrado y descifrado (dummy functions para ejemplificar)
def encrypt_cesar(message, alphabet, key):
    encrypted_message = ''
    for char in message:
        if char in alphabet:
            # Find the current position of the character
            original_index = alphabet.index(char)
            # Calculate the new position with the key
            new_index = (original_index + key) % len(alphabet)
            # Append the encrypted character to the result
            encrypted_message += alphabet[new_index]
        else:
            # If the character is not in the alphabet, keep it unchanged
            encrypted_message += char
    return encrypted_message

def decrypt_cesar(message, alphabet, key):
    decrypted_message = ''
    for char in message:
        if char in alphabet:
            # Find the current position of the character
            encrypted_index = alphabet.index(char)
            # Calculate the original position with the key
            original_index = (encrypted_index - key) % len(alphabet)
            # Append the decrypted character to the result
            decrypted_message += alphabet[original_index]
        else:
            # If the character is not in the alphabet, keep it unchanged
            decrypted_message += char
    return decrypted_message

def encrypt_monoalfabetico(message):
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
            if char.isupper():
                encrypted_message += encrypted_char.upper()
            else:
                encrypted_message += encrypted_char
        else:
            encrypted_message += char

    return encrypted_message

def decrypt_monoalfabetico(encrypted_message):
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
            if char.isupper():
                decrypted_message += decrypted_char.upper()
            else:
                decrypted_message += decrypted_char
        else:
            decrypted_message += char

    return decrypted_message

def encrypt_playfair(message, key):
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

def decrypt_playfair(ciphertext, key):
    # Validar y limpiar el texto cifrado
    ciphertext = ciphertext.upper().replace(" ", "").replace("Ñ", "N")
    ciphertext = ''.join(filter(str.isalpha, ciphertext))

    # Validar y limpiar la clave
    key = key.upper().replace(" ", "").replace("Ñ", "N")
    key = ''.join(filter(str.isalpha, key))

    if not key.isalpha():
        raise ValueError("La clave solo debe contener letras y no puede incluir caracteres especiales o espacios.")

    # Eliminar caracteres duplicados de la clave
    key = ''.join(sorted(set(key), key=lambda x: key.index(x)))

    # Crear la matriz 5x5 usando la clave
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    matrix = []
    for char in key:
        if char in alphabet:
            matrix.append(char)
            alphabet = alphabet.replace(char, "")
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

    pairs = split_into_pairs(ciphertext)

    # Descifrar cada par de letras
    decrypted_message = []
    for pair in pairs:
        row1, col1 = get_position(pair[0])
        row2, col2 = get_position(pair[1])

        if row1 == row2:
            decrypted_message.append(matrix_5x5[row1][(col1 - 1) % 5])
            decrypted_message.append(matrix_5x5[row2][(col2 - 1) % 5])
        elif col1 == col2:
            decrypted_message.append(matrix_5x5[(row1 - 1) % 5][col1])
            decrypted_message.append(matrix_5x5[(row2 - 1) % 5][col2])
        else:
            decrypted_message.append(matrix_5x5[row1][col2])
            decrypted_message.append(matrix_5x5[row2][col1])

    return ''.join(decrypted_message)


def encrypt_hill(plaintext, key_matrix):
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
        block_vector = np.array([char_to_num(char) for char in block]).reshape(-1, 1)
        encrypted_vector = np.dot(key_matrix, block_vector) % 26
        encrypted_message.extend([num_to_char(num) for num in encrypted_vector.flatten()])

    return ''.join(encrypted_message)

def mod_inverse(matrix, mod):
    # Utiliza sympy para calcular la inversa modular de una matriz
    det = int(round(np.linalg.det(matrix)))  # Determinante de la matriz
    det_inv = pow(det, -1, mod)  # Inversa del determinante módulo 26
    matrix_mod_inv = det_inv * np.round(det * np.linalg.inv(matrix)).astype(int) % mod
    return matrix_mod_inv

def decrypt_hill(ciphertext, key_matrix):
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
        block_vector = np.array([char_to_num(char) for char in block]).reshape(-1, 1)
        decrypted_vector = np.dot(key_matrix_inv, block_vector) % 26
        decrypted_message.extend([num_to_char(num) for num in decrypted_vector.flatten()])

    return ''.join(decrypted_message)

def string_to_matrix(matrix_string):
    # Limpiar la cadena eliminando espacios en blanco innecesarios
    matrix_string = matrix_string.strip()

    # Convertir la cadena en una lista de enteros, ignorando elementos vacíos
    matrix_list = list(map(int, filter(None, matrix_string.split(','))))

    # Calcular el tamaño de la matriz (debe ser cuadrada)
    size = int(len(matrix_list) ** 0.5)
    if size * size != len(matrix_list):
        raise ValueError("La clave debe formar una matriz cuadrada.")

    # Convertir la lista en una matriz 2D
    matrix = np.array(matrix_list).reshape(size, size)
    return matrix

if __name__ == '__main__':
    app.run(debug=True)