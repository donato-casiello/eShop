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
    .then(result => {console.log(result);
        // Check if the item is in the cart or not and update the cart item count
        console.log(result.added_to_cart);
        if(result && result.added_to_cart === false) {
            let cartCount = document.getElementById('cartCount');
            let newCount = parseInt(cartCount.innerHTML) + 1;
            cartCount.innerHTML = newCount;
            console.log(newCount);
        }})
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