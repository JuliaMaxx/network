document.addEventListener('DOMContentLoaded', () => {
    
    document.querySelectorAll('.bi-heart-fill').forEach((heart) => {
        const id = heart.parentElement.dataset.id;
        const user_id = heart.parentElement.dataset.user;
        console.log(user_id);
        fetch(`/likes/${id}/${user_id}`)
        .then(response => response.json())
        .then(data => {
            heart.parentElement.parentElement.querySelector('.num_likes').innerHTML = data.likes
            if(data.liked){
                heart.setAttribute('fill', 'rgb(195, 16, 52)');
            }
            else{
                heart.setAttribute('fill', 'rgb(209, 209, 209)')
            }
        })   
        heart.addEventListener('click', () => {
            const fill = heart.getAttribute('fill');
            if (fill ===  'rgb(209, 209, 209)'){
                    fetch(`/likes/${id}/${user_id}`, {
                        method: 'POST'
                  })
                  .then(response => response.json())
                  .then(result => {
                    console.log(result);
                  });
                  fetch(`/likes/${id}/${user_id}`)
                  .then(response => response.json())
                  .then(data => {
                      heart.parentElement.parentElement.querySelector('.num_likes').innerHTML = data.likes
                  })   
                heart.setAttribute('fill', 'rgb(195, 16, 52)');
            }
            else{
                fetch(`/likes/${id}/${user_id}`, {
                        method: 'PUT'
                })
                .then(response => response.json())
                .then(result => {
                    console.log(result);
                });
                fetch(`/likes/${id}/${user_id}`)
                  .then(response => response.json())
                  .then(data => {
                      heart.parentElement.parentElement.querySelector('.num_likes').innerHTML = data.likes
                  })   
                heart.setAttribute('fill', 'rgb(209, 209, 209)')
            }     
        })
    })
})