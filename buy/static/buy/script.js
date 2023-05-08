
// Show the modal to inform that the item was added to cart
function addToCart(slug){
    console.log(slug)
    fetch(`/buy/add-to-cart/${slug}`, {
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
            // Update the cartCount 
            let cartCount = document.getElementById('cartCount');
            let newCount = parseInt(cartCount.innerHTML) + 1;
            cartCount.innerHTML = newCount;
        }
    })
}

// Handle the cookies
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if(parts.length == 2) return parts.pop().split(';').shift(); 
    }