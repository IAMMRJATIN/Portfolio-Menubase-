var typed = new Typed('.typed-text', {
  strings: ["Programmer", "Developer", "Designer", "AI anthuziast"],
  typeSpeed: 60,
  backSpeed: 30,
  loop: true
});

document.addEventListener('mousemove', function(event) {
    const glitter = document.createElement('div');
    glitter.className = 'glitter';
    glitter.style.left = `${event.pageX}px`;
    glitter.style.top = `${event.pageY}px`;
    
    document.body.appendChild(glitter);
    
    setTimeout(() => {
        glitter.remove();
    }, 200);
});
