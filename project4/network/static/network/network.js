const buttons = document.querySelectorAll('.edit');
const contents = document.querySelectorAll('.post_content');
buttons.forEach((button) => {
    button.addEventListener('click', () => {
        if (button.innerHTML === 'Edit'){
            button.innerHTML = 'Save';
            contents.forEach((content) => {
                if (content.dataset.id === button.dataset.id){
                    content.innerHTML = `
                    <form class="edit_form" action="${url_index}" method="post" id='form1'>
                        ${csrf_token}
                        <input type="hidden" value="${content.dataset.id}" name="pk">
                        <input class="input_edit" name="edit" type="textarea" autofocus autocomplete="off" value=" ${content.dataset.content}">
                        <button type="submit" style="display: none;"></button>
                    </form>`;
                    const inputEdit = content.querySelector('.input_edit');
                    inputEdit.focus();
                    
                }
            })
        }
        else{
            const form = document.getElementById('form1');
            form.querySelector('button[type="submit"]').click();
            button.innerHTML = 'Edit';
            contents.forEach((content) => {
                if (content.dataset.id === button.dataset.id){  
                    const inputEdit = content.querySelector('.input_edit');
                    content.innerHTML = inputEdit.value;
                }
            })
        }
    })
})