document.addEventListener('DOMContentLoaded', function() {
    // Obtener el elemento del interruptor de tema (modo oscuro/claro)
    const themeSwitch = document.getElementById('theme-switch');

    // Obtener el control de volumen
    const volumeControl = document.getElementById('volume');

    // Crear un nuevo objeto de audio y asignar la ruta del archivo de música de fondo
    const audio = new Audio('/static/music/background.mp3');

    // Configurar la música de fondo para que se reproduzca en bucle
    audio.loop = true;
    audio.id = 'background-music';

    // Agregar el elemento de audio al final del cuerpo del documento
    document.body.appendChild(audio);

    // Obtener el volumen guardado en la cookie, o usar un valor por defecto de '0'
    const volume = getCookie('volume') || '0'; 

    // Establecer el volumen del audio basado en el valor de la cookie
    audio.volume = parseFloat(volume);

    // Si el control de volumen existe, ajustar su valor para reflejar el volumen actual
    if (volumeControl) {
        volumeControl.value = audio.volume * 100;
    }

    // Iniciar la reproducción del audio
    audio.play();

    // Si el interruptor de tema existe, ajustar su estado para reflejar el tema actual
    if (themeSwitch) {
        themeSwitch.checked = document.body.classList.contains('dark-mode');

        // Agregar un evento de cambio al interruptor de tema
        themeSwitch.addEventListener('change', function() {
            // Alternar la clase 'dark-mode' en el cuerpo del documento
            document.body.classList.toggle('dark-mode');

            // Enviar una solicitud para actualizar el estado del modo oscuro en el servidor
            fetch(`/set_dark_mode/${themeSwitch.checked ? 1 : 0}`);
        });
    }

    // Si el control de volumen existe, agregar un evento de entrada para ajustar el volumen
    if (volumeControl) {
        volumeControl.addEventListener('input', function() {
            // Obtener el valor del control de volumen y ajustarlo para el audio
            const volumeValue = volumeControl.value / 100;
            audio.volume = volumeValue;

            // Establecer la cookie de volumen con el nuevo valor
            setCookie('volume', volumeValue, 365);

            // Enviar una solicitud para actualizar el volumen en el servidor
            fetch(`/set_volume/${volumeValue}`);
        });
    }
});

// Función para cambiar el idioma de la aplicación
function setLanguage(language) {
    // Enviar una solicitud para cambiar el idioma en el servidor y recargar la página
    fetch(`/set_language/${language}`).then(() => location.reload());
}

// Función para obtener el valor de una cookie por su nombre
function getCookie(name) {
    // Obtener todas las cookies y buscar la cookie con el nombre dado
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

// Función para establecer una cookie con un nombre, valor y número de días hasta que expire
function setCookie(name, value, days) {
    let expires = '';
    if (days) {
        // Calcular la fecha de expiración basada en el número de días
        const date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = `; expires=${date.toUTCString()}`;
    }
     // Configurar la cookie con el nombre, valor y fecha de expiración (si se proporciona)
    document.cookie = `${name}=${value || ''}${expires}; path=/`;
}
