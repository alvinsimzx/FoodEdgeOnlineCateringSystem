window.addEventListener('scroll', function(){
    const parallax = document.querySelector('.bigBanner');
    const opacity = document.querySelector('.opacity');
    let scroll = window.pageYOffset;

    parallax.style.transform = 'translateY('+ scroll*.3+'px)';
    opacity.style.opacity =  scroll / (sectionY.top + section_height);
})
