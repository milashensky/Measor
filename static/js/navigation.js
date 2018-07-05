window.addEventListener("load", function(event) {
    elements = document.querySelectorAll('.nav-link');
    for (let i = 0, el; el = elements[i]; i++){
        if (el.href == window.location.href){
            el.classList.add('active')
        } else {
            el.classList.remove('active')
        }
    }
})
