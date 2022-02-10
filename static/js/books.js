'use strict';

let buttons = document.querySelectorAll('.delete-button');

for (const button of buttons){
    button.addEventListener('click', (evt) => { 

        console.log(evt.target.id)
    //callback function
        const formInputs = {
            favoriteIdDelete: evt.target.id
        };
        // const deleteFavorite = document.querySelector('li').remove();
    
        fetch('/delete', {
            method: 'POST',
            body: JSON.stringify(formInputs),
            headers:{
                'Content-Type': 'application/json',
            },
        
        })
            // return nothing but reload page with update
            .then(response => response.json())
            .then(responseJson => {
                // window.location.reload(true);
                console.log(responseJson);
                // alert(responseJson.status);
                window.location.href='http://localhost:5000/user/profile';
            });
    });
    
    
}

buttons = document.querySelectorAll('.edit-button');

for (const button of buttons){
    button.addEventListener('click', (evt) => { 
        console.log(evt)
        console.log(evt.target)
        console.log(evt.target.id)
        
        const favorite_id = evt.target.parentNode.dataset.favoriteId;
        
        const input_comment = evt.target.parentNode.childNodes[1].childNodes[5];
        const text = input_comment.innerHTML;
        input_comment.innerHTML = " ";
        const input = document.createElement("input");
        input.type = "text";
        input.defaultValue = text;
        input_comment.appendChild(input);
        const save_button = document.createElement("button");
        save_button.innerHTML =  "save";
        save_button.addEventListener('click', (evt) => {
            const formInputs = {
                favoriteIdEdit: favorite_id,
                comment: input.value
            };
            
            console.log(input.innerHTML);
            fetch('/edit', {
                method: 'POST',
                body: JSON.stringify(formInputs),
                headers:{
                    'Content-Type': 'application/json',
                },
            
            })
                // return nothing but reload page with update
                .then(response => response.json())
                .then(responseJson => {
                    // window.location.reload(true);
                    console.log(responseJson);
                    // alert(responseJson.status);
                    window.location.href='http://localhost:5000/user/profile';
                });
            

            });
        input_comment.appendChild(save_button);
    //callback function
        

    });
    
}



