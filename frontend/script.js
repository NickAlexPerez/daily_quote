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
