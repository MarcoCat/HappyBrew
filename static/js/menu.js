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