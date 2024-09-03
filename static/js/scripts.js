document.addEventListener('DOMContentLoaded', function() {
    const themeSwitch = document.getElementById('theme-switch');
    const volumeControl = document.getElementById('volume');
    const audio = new Audio('/static/music/background.mp3');

    audio.loop = true;
    audio.id = 'background-music';
    document.body.appendChild(audio);

    const volume = getCookie('volume') || '0'; 
    audio.volume = parseFloat(volume);
    if (volumeControl) {
        volumeControl.value = audio.volume * 100;
    }

    audio.play();

    if (themeSwitch) {
        themeSwitch.checked = document.body.classList.contains('dark-mode');
        themeSwitch.addEventListener('change', function() {
            document.body.classList.toggle('dark-mode');
            fetch(`/set_dark_mode/${themeSwitch.checked ? 1 : 0}`);
        });
    }

    if (volumeControl) {
        volumeControl.addEventListener('input', function() {
            const volumeValue = volumeControl.value / 100;
            audio.volume = volumeValue;
            // Establecer la cookie de volumen al cambiar
            setCookie('volume', volumeValue, 365);
            fetch(`/set_volume/${volumeValue}`);
        });
    }
});

function setLanguage(language) {
    fetch(`/set_language/${language}`).then(() => location.reload());
}

// Función para obtener el valor de una cookie por su nombre
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

// Función para establecer una cookie
function setCookie(name, value, days) {
    let expires = '';
    if (days) {
        const date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = `; expires=${date.toUTCString()}`;
    }
    document.cookie = `${name}=${value || ''}${expires}; path=/`;
}
