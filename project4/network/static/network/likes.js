document.addEventListener('DOMContentLoaded', () => {
    
    document.querySelectorAll('.bi-heart-fill').forEach((heart) => {
        const id = heart.parentElement.dataset.id;
        console.log(id);
        fetch(`/likes/${id}`)
        .then(response => response.json())
        .then(data => {
            heart.parentElement.parentElement.querySelector('.num_likes').innerHTML = data.likes
        })   
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