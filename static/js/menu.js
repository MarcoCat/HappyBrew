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

document.getElementById('user-info-form').addEventListener('submit', async (e) => {
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
  // Retrieve the updated cart from local storage after adding products
  let cart = JSON.parse(localStorage.getItem('cart')) || [];
  
  // Create a new FormData object to store the data you want to send to the server
  const postData = new FormData();
  postData.append('name', name);
  postData.append('address', address);
  cart.forEach((item, index) => {
    postData.append(`products[${index}][name]`, item.name);
    postData.append(`products[${index}][quantity]`, item.quantity);
  });

  // Send a POST request to the /order endpoint with the form data
  const response = await fetch('/order', {
    method: 'POST',
    body: postData,
  });

  // If the request is successful, redirect to the cart page
  if (response.ok) {
    window.location.href = '/cart';
    localStorage.removeItem('cart');
  } else {
    console.error('Error while creating the order:', await response.text());
  }
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
  
document.querySelectorAll('.addButton').forEach(button => {
  button.addEventListener('click', () => {
      const countInput = button.previousElementSibling;
      countInput.value = parseInt(countInput.value) + 1;
  });
});

document.querySelectorAll('.removeButton').forEach(button => {
  button.addEventListener('click', () => {
      const countInput = button.nextElementSibling;
      countInput.value = Math.max(0, parseInt(countInput.value) - 1);
  });
});