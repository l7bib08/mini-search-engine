async function performSearch() {
    const query = document.getElementById("searchInput").value;

    const response = await fetch(`http://127.0.0.1:8000/search?q=${query}`);
    const data = await response.json();

    const resultsDiv = document.getElementById("results");
    resultsDiv.innerHTML = "";

    if (data.length === 0) {
        resultsDiv.innerHTML = "<p>No results found</p>";
        return;
    }

    data.forEach(result => {
        const div = document.createElement("div");

        div.innerHTML = `
            <h3>${result.title}</h3>
            <a href="${result.url}" target="_blank">${result.url}</a>
            <p><strong>Score:</strong> ${result.score}</p>
            <p>${result.snippet}...</p>
            <hr>
        `;

        resultsDiv.appendChild(div);
    });
}