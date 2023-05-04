document.addEventListener("DOMContentLoaded", function(){


})

// Show the modal to inform that the item was added to cart
function addToCart(){
    const modal = document.getElementById('overlay');   
    console.log(modal)
    modal.style.display = "block";

}

// Close the modal
function closeModal(){
    const modal = document.getElementById('overlay');   
    console.log(modal)
    modal.style.display = "none";
}
