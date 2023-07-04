document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.bi-heart-fill').forEach((heart) => {
        heart.addEventListener('click', () => {
            const fill = heart.getAttribute('fill');
            if (fill ===  'rgb(209, 209, 209)'){
                heart.setAttribute('fill', 'rgb(195, 16, 52)');
            }
            else{
                heart.setAttribute('fill', 'rgb(209, 209, 209)')
            }
        
            
        })
    })
})