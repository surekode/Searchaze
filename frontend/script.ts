

document.getElementById("searchForm").addEventListener("submit", function(event) {
    event.preventDefault();
    const query = (document.getElementById("searchInput") as HTMLInputElement).value.trim();
    search(query);
});

function search(query: string): void {
    fetch(`/search?query=${query}`)
        .then(response => response.json())
        .then(data => displayResults(data.results))
        .catch(error => console.error("Error:", error));
}

function displayResults(results: string[]): void {
    const searchResults = document.getElementById("searchResults");
    searchResults.innerHTML = "";

    if (results.length === 0) {
        searchResults.textContent = "No results found.";
    } else {
        const ul = document.createElement("ul");
        results.forEach(result => {
            const li = document.createElement("li");
            li.textContent = result;
            ul.appendChild(li);
        });
        searchResults.appendChild(ul);
    }
}
