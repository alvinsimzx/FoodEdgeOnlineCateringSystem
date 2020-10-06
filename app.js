window.addEventListener('scroll', function(){
    const parallax = document.querySelector('.bigBanner');
    let scroll = window.pageYOffset;

    parallax.style.transform = 'translateY('+ scroll*.3+'px)';
})