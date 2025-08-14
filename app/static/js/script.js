function getQuote() {
  fetch("http://localhost:5000/quote")
    .then(response => response.json())
    .then(data => {
      document.getElementById("quote").innerText = data.quote;
    })
    .catch(err => {
      document.getElementById("quote").innerText = "Error fetching quote.";
      console.error(err);
    });
}

function loadQuoteTable() {
  fetch("http://localhost:5000/quotes")
    .then(response => response.json())
    .then(data => {
      const tableBody = document.querySelector("#quote-table tbody");
      tableBody.innerHTML = "";  // Clear existing rows

      data.forEach(quote => {
        const row = document.createElement("tr");

        const idCell = document.createElement("td");
        idCell.textContent = quote.id;

        const textCell = document.createElement("td");
        const input = document.createElement("input");
        input.type = "text";
        input.value = quote.text;
        input.size = 50;
        textCell.appendChild(input);

        const actionCell = document.createElement("td");
        const saveButton = document.createElement("button");
        saveButton.textContent = "Save";
        saveButton.onclick = () => updateQuote(quote.id, input.value);
        actionCell.appendChild(saveButton);

        const deleteButton = document.createElement("button");
        deleteButton.textContent = "Delete";
        deleteButton.onclick = () => deleteQuote(quote.id);
        actionCell.appendChild(deleteButton);

        row.appendChild(idCell);
        row.appendChild(textCell);
        row.appendChild(actionCell);

        tableBody.appendChild(row);
      });
    })
    .catch(error => {
      console.error("Error loading quotes:", error);
    });
}


function addQuote() {
  const newQuote = document.getElementById("new-quote").value.trim();
  if (!newQuote) {
    alert("Please enter a quote.");
    return;
  }

  fetch("http://localhost:5000/quote", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ quote: newQuote })
  })
    .then(response => {
      if (!response.ok) throw new Error("Failed to add quote");
      return response.json();
    })
    .then(data => {
      document.getElementById("add-quote-message").innerText = data.message;
      document.getElementById("new-quote").value = "";
      loadQuoteTable();
    })
    .catch(error => {
      document.getElementById("add-quote-message").innerText = "Error adding quote.";
      console.error(error);
    });
}

function updateQuote(id, newText) {
  fetch(`http://localhost:5000/quote/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text: newText })
  })
    .then(res => res.json())
    .then(data => {
      alert(data.message || "Updated.");
    })
    .catch(err => console.error("Error updating quote:", err));
}

function deleteQuote(id) {
  if (!confirm("Are you sure you want to delete this quote?")) return;

  fetch(`http://localhost:5000/quote/${id}`, {
    method: "DELETE"
  })
    .then(res => {
      if (!res.ok) throw new Error("Failed to delete quote");
      return res.json();
    })
    .then(data => {
      alert(data.message || "Deleted.");
      loadQuoteTable();
    })
    .catch(err => console.error("Error deleting quote:", err));
}

window.onload = function () {
  getQuote();       // existing random quote function
  loadQuoteTable(); // new
};
