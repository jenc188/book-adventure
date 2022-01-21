'use strict';

const buttons = document.querySelectorAll('.delete-button');

for (const button of buttons){
    button.addEventListener('click', (evt) => { 

        console.log(evt.target.id)
       
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

            .then(response => response.json())
            .then(responseJson => {
                // window.location.reload(true);
                console.log(responseJson);
                // alert(responseJson.status);
                window.location.href='http://localhost:5000/user/profile';
            });
    });
    
}




