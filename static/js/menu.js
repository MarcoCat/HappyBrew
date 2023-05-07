// Add to cart function
function addToCart(productName, productPrice, quantity) {
  // Retrieve cart from local storage, parse it and store in the variable cart
  let cart = JSON.parse(localStorage.getItem('cart')) || [];

  // Check if the product already exists in the cart
  let productIndex = cart.findIndex(item => item.name === productName);

  // If the product exists, update the quantity; else, add a new item to the cart
  if (productIndex !== -1) {
    cart[productIndex].quantity += quantity;
  } else {
    cart.push({ name: productName, price: productPrice, quantity });
  }

  // Save the updated cart back to local storage
  localStorage.setItem('cart', JSON.stringify(cart));
}

document.getElementById('order-form').addEventListener('submit', (e) => {
  e.preventDefault();
  const formData = new FormData(e.target);
  const name = formData.get('name');
  const address = formData.get('address');

  document.querySelectorAll('.count').forEach((countInput, index) => {
    const quantity = parseInt(countInput.value);
    if (quantity > 0) {
      const productName = countInput.parentElement.querySelector('h3').textContent;
      const productPrice = parseFloat(countInput.parentElement.querySelector('.addToCartButton').dataset.price);
      addToCart(productName, productPrice, quantity);
    }
  });

  // Redirect to the cart page
  window.location.href = '/cart';
});
// Get all the buttons with class "addToCartButton"
const addToCartButtons = document.querySelectorAll('.addToCartButton');

// Add event listener to each button
addToCartButtons.forEach(button => {
  button.addEventListener('click', () => {
    // Get the count input element for the clicked button
    const countInput = button.parentElement.querySelector('.count');
    const quantity = parseInt(countInput.value);

    // Get the product name for the clicked button
    const productName = button.parentElement.querySelector('h3').textContent;

   // Get the product price for the clicked button
   const productPrice = parseFloat(button.dataset.price);

   // Call addToCart function with the product name, price, and quantity
   addToCart(productName, productPrice, quantity);
 });
});
  
  // Get all the buttons with class "addButton"
  const addButtons = document.querySelectorAll('.addButton');
  
  // Add event listener to each button
  addButtons.forEach(button => {
    button.addEventListener('click', () => {
      // Get the count input element for the clicked button
      const countInput = button.previousElementSibling;
      // Increase the value of the input element by 1
      countInput.value = parseInt(countInput.value) + 1;
    });
  });

  // Get all the buttons with class "removeButton"
  const removeButtons = document.querySelectorAll('.removeButton');
  
  // Add event listener to each button
  removeButtons.forEach(button => {
    button.addEventListener('click', () => {
      // Get the count input element for the clicked button
      const countInput = button.nextElementSibling;
      // Decrease the value of the input element by 1, but don't go below 1
      countInput.value = parseInt(countInput.value) - 1 < 1 ? 1 : parseInt(countInput.value) - 1;
    });
  });