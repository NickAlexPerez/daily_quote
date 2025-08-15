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

        const tagsCell = document.createElement("td");
        tagsCell.id = `tags-cell-${quote.id}`;

        const tagSelect = document.createElement("select");
        tagSelect.id = `new-tag-${quote.id}`;


        fetch(`http://localhost:5000/quote/${quote.id}/available-tags`)
          .then(response => response.json())
          .then(tags => {
            tags.forEach(tag => {
              const option = document.createElement("option");
              option.value = tag.id;
              option.textContent = tag.name;
              tagSelect.appendChild(option);
            });
          });

        const addTagButton = document.createElement("button");
        addTagButton.textContent = "Add Tag";
        addTagButton.onclick = () => addTagToQuote(quote.id, tagSelect.value);

        const existingTagList = document.createElement("div");
        existingTagList.id = `tag-list-${quote.id}`;
        tagsCell.appendChild(existingTagList);

        tagsCell.appendChild(tagSelect);
        tagsCell.appendChild(addTagButton);

        fetch(`http://localhost:5000/quote/${quote.id}/tags`)
          .then(response => response.json())
          .then(tags => {
            const tagList = document.getElementById(`tag-list-${quote.id}`);
            tagList.innerHTML = ""; // Clear existing tags
            tags.forEach(tag => {
              const tagItem = document.createElement("span");
              tagItem.className = "tag-chip";
              tagItem.innerHTML = `${tag.name} <button class="remove-tag">x</button>`;
              tagItem.querySelector(".remove-tag")
                .onclick = () => removeTagFromQuote(quote.id, tag.id);
              tagList.appendChild(tagItem);
            });
          })
          .catch(err => {
            console.error("Error fetching tags:", err);
          });

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
        row.appendChild(tagsCell);

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

function loadTagTable() {
  fetch("http://localhost:5000/tags")
    .then(response => response.json())
    .then(data => {
      const tableBody = document.querySelector("#tag-table tbody");
      tableBody.innerHTML = "";  // Clear existing rows

      data.forEach(tag => {
        const row = document.createElement("tr");

        const idCell = document.createElement("td");
        idCell.textContent = tag.id;

        const nameCell = document.createElement("td");
        const input = document.createElement("input");
        input.type = "text";
        input.value = tag.name;
        input.size = 50;
        nameCell.appendChild(input);

        const actionCell = document.createElement("td");
        const saveButton = document.createElement("button");
        saveButton.textContent = "Save";
        saveButton.onclick = () => updateTag(tag.id, input.value);
        actionCell.appendChild(saveButton);

        const deleteButton = document.createElement("button");
        deleteButton.textContent = "Delete";
        deleteButton.onclick = () => deleteTag(tag.id);
        actionCell.appendChild(deleteButton);

        row.appendChild(idCell);
        row.appendChild(nameCell);
        row.appendChild(actionCell);

        tableBody.appendChild(row);
      });
    })
    .catch(error => {
      console.error("Error loading tags:", error);
    });
}

function addTag() {
  const newTag = document.getElementById("new-tag").value.trim();
  if (!newTag) {
    alert("Please enter a tag.");
    return;
  }

  fetch("http://localhost:5000/tag", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ name: newTag })
  })
    .then(response => {
      if (!response.ok) throw new Error("Failed to add tag");
      return response.json();
    })
    .then(data => {
      document.getElementById("add-tag-message").innerText = data.message;
      document.getElementById("new-tag").value = "";
      loadTagTable();
    })
    .catch(error => {
      document.getElementById("add-tag-message").innerText = "Error adding tag.";
      console.error(error);
    });
}

function updateTag(id, newName) {
  fetch(`http://localhost:5000/tag/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name: newName })
  })
    .then(res => res.json())
    .then(data => {
      alert(data.message || "Updated.");
      loadTagTable();
    })
    .catch(err => console.error("Error updating tag:", err));
}

function deleteTag(id) {
  if (!confirm("Are you sure you want to delete this tag?")) return;

  fetch(`http://localhost:5000/tag/${id}`, {
    method: "DELETE"
  })
    .then(res => {
      if (!res.ok) throw new Error("Failed to delete tag");
      return res.json();
    })
    .then(data => {
      alert(data.message || "Deleted.");
      loadTagTable();
    })
    .catch(err => console.error("Error deleting tag:", err));
}

function addTagToQuote(quoteId, tagID) {
  if (!tagID) {
    alert("Please enter a tag.");
    return;
  }

  fetch(`http://localhost:5000/quote/${quoteId}/tag`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ tag_id: tagID })
  })
    .then(response => {
      if (!response.ok) throw new Error("Failed to add tag to quote");
      return response.json();
    })
    .then(data => {
      alert(data.message || "Tag added to quote.");
      loadQuoteTable();
    })
    .catch(error => {
      console.error("Error adding tag to quote:", error);
    });
}

function removeTagFromQuote(quoteId, tagId) {
  fetch(`http://localhost:5000/quote/${quoteId}/tag/${tagId}`, {
    method: "DELETE"
  })
    .then(response => {
      if (!response.ok) throw new Error("Failed to remove tag from quote");
      return response.json();
    })
    .then(data => {
      alert(data.message || "Tag removed from quote.");
      loadQuoteTable();
    })
    .catch(error => {
      console.error("Error removing tag from quote:", error);
    });
}

window.onload = function () {
  getQuote();       // existing random quote function
  loadQuoteTable(); // new
  loadTagTable();   // new tag loading function
};
