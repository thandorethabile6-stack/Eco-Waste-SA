function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                document.getElementById('latitude_x').value = position.coords.latitude
                document.getElementById('longitude_y').value = position.coords.longitude
            }, () => {
                document.getElementById('geo_enabled').value = 'No'
            }
        )
    }
    else {
        document.getElementById('geo_avail').value = 'No'
    }
}

// Auto-hide flash messages after 5 seconds
setTimeout(() => {
    const messages = document.querySelectorAll('.flashed-messages');
    messages.forEach(msg => {
        msg.style.opacity = '0';
        setTimeout(() => msg.remove(), 600);
    });
}, 5000);

const navs = document.querySelectorAll('.nav-link')

if (document.URL.endsWith('/')) {
    navs.forEach(link => { link.classList.remove('active') })
    navs[0].classList.add('active')
}
if (document.URL.endsWith('/posts')) {
    navs.forEach(link => { link.classList.remove('active') })
    navs[1].classList.add('active')
}
if (document.URL.endsWith('/analytics')) {
    navs.forEach(link => { link.classList.remove('active') })
    navs[2].classList.add('active')
}
if (document.URL.endsWith('/map')) {
    navs.forEach(link => { link.classList.remove('active') })
    navs[3].classList.add('active')
}
if (document.URL.endsWith('/learn')) {
    navs.forEach(link => { link.classList.remove('active') })
    navs[4].classList.add('active')
}

