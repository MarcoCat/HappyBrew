
// menu page

function subtractOne(button) {
    var input = button.nextElementSibling;
    var value = parseInt(input.value);
    if (value >= 1) {
        input.value = value - 1;
    }
}

function addOne(button) {
    var input = button.previousElementSibling;
    var value = parseInt(input.value);
    input.value = value + 1;
}

function getOrderSummary() {
    var orderSummary = {};

    var name = document.getElementById("name").value;
    var address = document.getElementById("address").value;
    orderSummary.name = name;
    orderSummary.address = address;
    orderSummary.products = {};

    var categories = document
        .getElementsByClassName("menuItem")[0]
        .getElementsByTagName("h2");

    for (var i = 0; i < categories.length; i++) {
        var category = categories[i];
        var categoryName = category.id;
        var itemsContainer = category.nextElementSibling;
        var items = itemsContainer.querySelectorAll(".itemType li");

        for (var j = 0; j < items.length; j++) {
        var item = items[j];
        var itemName = item.getElementsByTagName("h3")[0].textContent;
        var countInput = item.getElementsByClassName("count")[0];
        var itemCount = parseInt(countInput.value);

        if (itemCount > 0) {
            if (!orderSummary.products[categoryName]) {
            orderSummary.products[categoryName] = [];
            }

            orderSummary.products[categoryName].push({
            name: itemName,
            count: itemCount,
            });
        }
        }
    }

    return JSON.stringify(orderSummary);
}


async function submitOrder() {
    const order_summary = getOrderSummary();
    const authStatus = document.getElementById("authStatus").value;

    if (authStatus === "false") {
    alert("Login required. Please log in first.");
    return;
    }

    try {
    const response = await fetch("/order", {
        method: "POST",
        headers: {
        "Content-Type": "application/json",
        },
        body: JSON.stringify(order_summary),
    });

    if (response.ok) {
        alert("Thank you for your ordering!");
        const data = await response.json();
        window.location.href = data.location;
    } else {
        const errorData = await response.json();
        alert(errorData.error);
    }
    } catch (error) {
    console.error("Error ordering:", error);
    }
}


// customize page


  var selectedItems = {};

  function selectItem(button, itemName, itemCategory) {
    if (itemCategory !== "Toppings") {
      var buttons = document.querySelectorAll(
        `button[data-category="${itemCategory}"]`
      );
      console.log(buttons);

      // Deselect all buttons in the category except for Toppings
      buttons.forEach(function (btn) {
        if (btn.dataset.category !== "Toppings") {
          btn.classList.remove("selected");
          delete selectedItems[btn.dataset.category];
        }
      });
    }

    if (button.classList.contains("selected")) {
      button.classList.remove("selected");
      if (itemCategory in selectedItems) {
        const categoryItems = selectedItems[itemCategory];
        const itemIndex = categoryItems.indexOf(itemName);
        if (itemIndex !== -1) {
          categoryItems.splice(itemIndex, 1);
          if (categoryItems.length === 0) {
            delete selectedItems[itemCategory];
          }
        }
      }
    } else {
      if (itemCategory === "Toppings") {
        var toppingsCount = Object.keys(selectedItems["Toppings"] || {}).length;
        if (toppingsCount >= 3) {
          // Limit the toppings to 3 items
          alert("You can select up to 3 toppings.");
          return;
        }
      }

      button.classList.add("selected");
      if (!(itemCategory in selectedItems)) {
        selectedItems[itemCategory] = [];
      }
      selectedItems[itemCategory].push(itemName);
    }
    console.log(selectedItems);
  }



  async function createDrink() {
  const authStatus = document.getElementById("authStatus").value;

  if (authStatus === "false") {
    alert("Login required. Please log in first.");
    return;
  }
    try {
          const response = await fetch("/customize", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(selectedItems),
          });

          if (response.ok) {
            const result = await response.json();
            alert("Item added to Menu!");
            window.location.href = result.url;
          } else {
            const errorData = await response.json();
            alert(errorData.error);
          }
        } catch (error) {
          console.error("Error:", error);
        }
    }

  
// feedback page



  function clearTextArea() {
    document.getElementById("feedback-textarea").value = "";
  }

  async function submitFeedback(event) {
    event.preventDefault();
    const message = document.getElementById("feedback-textarea").value;

    if (!message.trim()) {
      alert("Please enter a message.");
      return;
    }

    const feedback = {
      message: message,
    };

    try {
      const response = await fetch("/feedback", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(feedback),
      });
      clearTextArea();
      alert("Thank you for your feedback!");
    } catch (error) {
      console.error("Error saving feedback:", error);
    }
  }
