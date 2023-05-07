// Add to cart function
function addToCart(productName, quantity) {
  // Retrieve cart from local storage, parse it and store in the variable cart
  let cart = JSON.parse(localStorage.getItem('cart')) || [];

  // Check if the product already exists in the cart
  let productIndex = cart.findIndex(item => item.name === productName);

  // If product exists, update the quantity, else add a new item to the cart
  if (productIndex !== -1) {
    cart[productIndex].quantity += quantity;
  } else {
    cart.push({ name: productName, quantity });
  }

  // Save the updated cart back to local storage
  localStorage.setItem('cart', JSON.stringify(cart));
}

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

    // Call addToCart function with the product name and quantity
    addToCart(productName, quantity);
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