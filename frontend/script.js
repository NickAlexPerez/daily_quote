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
    })
    .catch(error => {
      document.getElementById("add-quote-message").innerText = "Error adding quote.";
      console.error(error);
    });
}
