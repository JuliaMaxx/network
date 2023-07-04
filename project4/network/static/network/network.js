document.addEventListener('DOMContentLoaded', () => {
    
    const buttons = document.querySelectorAll('.edit');
    const contents = document.querySelectorAll('.post_content');
    buttons.forEach((button) => {
        button.addEventListener('click', () => {

            if (button.innerHTML === 'Edit'){
                button.innerHTML = 'Save';

                contents.forEach((content) => {
                    if (content.dataset.id === button.dataset.id){
                        let val = '';
                        fetch(`/edited/${content.dataset.id}`)
                        .then(response => response.json())
                        .then(data => {
                            console.log(data);
                            val = data.text;
                            content.innerHTML = `
                                <input class="input_edit" name="edit" type="textarea" autofocus autocomplete="off" value="${val}">`;
                            const inputEdit = content.querySelector('.input_edit');
                            inputEdit.focus();
                        });       
                    }
                })
            }
            else{
                button.innerHTML = 'Edit';
                contents.forEach((content) => {
                    if (content.dataset.id === button.dataset.id){  
                        const inputEdit = content.querySelector('.input_edit');
                        const edited = inputEdit.value;
                        const id = content.dataset.id;
                        fetch('/edit', {
                            method: 'POST',
                            body: JSON.stringify({
                                id: id,
                                edited: edited
                            })
                          })
                          .then(response => response.json())
                          .then(result => {
                            console.log(result);
                          });
                          fetch(`/edited/${id}`)
                            .then(response => response.json())
                            .then(data => {
                            console.log(data);
                                content.innerHTML = data.text;
                            })      
                    }
                })
            }
        })
    })
})

