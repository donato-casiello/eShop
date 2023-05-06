document.addEventListener("DOMContentLoaded", function(){


})

// Show the modal to inform that the item was added to cart
function addToCart(slug){
    const modal = document.getElementById('overlay');   
    console.log(slug)
    modal.style.display = "block";
    fetch(`add-to-cart/${slug}`, {
        method : "POST", 
        headers : {"Content-type":"application/json", "X-CSRFToken":getCookie('csrftoken')},
        body : JSON.stringify({
            content : slug 
        })
    }) 
    .then(response => response.json())
    .then(result => console.log(result))
}

// Close the modal
function closeModal(){
    const modal = document.getElementById('overlay');   
    console.log(modal)
    modal.style.display = "none";
}


// Handle the cookies
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if(parts.length == 2) return parts.pop().split(';').shift(); 
    }