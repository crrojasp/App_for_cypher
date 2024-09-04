# Decryption

Proyecto simple de página web, versión poco estetica pero funcional para encriptar y desencriptar con los métodos enseñados en la materia de "INTRODUCCION A LA CRIPTOGRAFIA Y A LA SEGURIDAD DE LA INFORMACION" dada por el profesor Tovar de la universidad nacional de Colombia durante el periodo "2024-I"

## Tabla de Contenidos

- [Descripción](#descripción)
- [Instalación](#instalación)
- [Uso](#uso)
- [Contribución](#contribución)
- [Licencia](#licencia)
- [Contacto](#contacto)

## Descripción

Este proyecto es una aplicación que permite a los usuarios encriptar y desencriptar mensajes utilizando varios algoritmos de cifrado, incluyendo César, Monoalfabético, Playfair y Hill. La aplicación también permite ajustar el volumen de la música de fondo (todavía falta mejorar su funcionamiento) y cambiar entre modo oscuro y claro (Las tonalidades no muestran mucha compatibilidad). Se creo con la intención de aportar un sistema capaz de encriptar y desencriptar con los métodos más basicos pero usando una interfaz básica. Todo lo anterior mencionado para poder poseer una herramienta funcional y utilizable para el parcial de "INTRODUCCION A LA CRIPTOGRAFIA Y A LA SEGURIDAD DE LA INFORMACION" durante el semestre "2024-I"

## Instalación

1. Clona el repositorio:
    ```bash
    git clone https://github.com/crrojasp/App_for_cypher.git
    ```

2. Navega al directorio del proyecto:
    ```bash
    cd App_for_cypher
    ```

3. Crea un entorno virtual e instálalo:
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
    ```

4. Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

## Uso

1. Ejecuta la aplicación:
    ```bash
    flask run 
    ```
    ó
   ```bash
    python app.py 
    ```

3. Abre tu navegador y ve a `http://localhost:5000` ó `http://127.0.0.1:5000` para acceder a la aplicación.

4. Usa los botones para navegar entre las secciones de cifrado, descifrado, opciones y sobre mí.

## Contribución

1. Haz un fork del repositorio.
2. Crea una nueva rama:
    ```bash
    git checkout -b main
    ```
3. Realiza tus cambios y haz commit:
    ```bash
    git add .
    git commit -m "Descripción de los cambios"
    ```
4. Envía tus cambios a tu fork:
    ```bash
    git push origin main
    ```
5. Abre un pull request desde tu fork.

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

## Contacto

Cristian Alejandro Rojas Pitta - [crrojasp@unal.edu.co](mailto:crrojasp@unal.edu.co)

Repositorio del proyecto: [https://github.com/crrojasp/App_for_cypher](https://github.com/crrojasp/App_for_cypher)
