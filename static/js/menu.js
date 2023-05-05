  // Add event listener to all "Add to cart" buttons
const addToCartButtons = document.querySelectorAll('.addToCartButton');

addToCartButtons.forEach(button => {
  button.addEventListener('click', () => {
    // Get the product container element for the clicked button
    const productContainer = button.closest('.itemType li');

    // Extract the product name, price, and quantity from the HTML
    const productName = productContainer.querySelector('h3').textContent;
    const productPrice = parseFloat(productContainer.querySelector('p.price').textContent.split(':')[1].trim());
    const productQuantity = parseInt(productContainer.querySelector('input.count').value);

    // Create a JavaScript object with the product data
    const product = {
      name: productName,
      price: productPrice,
      quantity: productQuantity
    };

    // Add the product to the cart in localStorage
    let cartItems = JSON.parse(localStorage.getItem('cartItems')) || [];
    cartItems.push(product);
    localStorage.setItem('cartItems', JSON.stringify(cartItems));
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