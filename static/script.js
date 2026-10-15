
async function startCrawl() {
    const urls = document.getElementById("urls").value
        .split("\n")
        .map(url => url.trim())
        .filter(Boolean);

    const button = document.getElementById("crawlBtn");
    const message = document.getElementById("message");

    if (urls.length === 0) {
        message.textContent = "Please enter at least one URL.";
        return;
    }

    button.disabled = true;
    message.textContent = "Crawling websites... Please wait.";

    try {
        const response = await fetch("/api/crawl", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ urls })
        });

        const data = await response.json();

        if (!response.ok) {
            const errorMessage = Array.isArray(data.detail)
                ? data.detail.map(item => item.msg).join(", ")
                : data.detail || "Request failed";

            throw new Error(errorMessage);
        }

        // Display performance comparison
        document.getElementById("performance").hidden = false;

        document.getElementById("seqTime").textContent =
            `${data.sequential_time} seconds`;

        document.getElementById("asyncTime").textContent =
            `${data.async_time} seconds`;

        const improvement = data.async_time > 0
            ? data.sequential_time / data.async_time
            : null;

        document.getElementById("speedup").textContent =
            improvement === null
                ? "N/A"
                : `${improvement.toFixed(2)}×`;

        // Display results from both crawlers
        renderResults("seqResults", data.sequential_results);
        renderResults("asyncResults", data.async_results);

        message.textContent =
            "Crawling completed successfully!";

    } catch (error) {
        message.textContent = `Error: ${error.message}`;
    } finally {
        button.disabled = false;
    }
}


function renderResults(elementId, results) {
    const container = document.getElementById(elementId);

    container.replaceChildren();

    results.forEach(result => {
        const card = document.createElement("div");
        card.className = "result";

        const extractedData =
            result.extracted_data === undefined
                ? "No extracted data available"
                : typeof result.extracted_data === "string"
                    ? result.extracted_data
                    : JSON.stringify(
                        result.extracted_data,
                        null,
                        2
                    );

        const details = [
            `URL: ${result.url}`,
            `Status: ${result.status_code ?? "Failed"}`,
            `Type: ${result.content_type || "Unknown"}`,
            `Title: ${result.title || "No title"}`,
            `Links: ${result.links_found ?? 0}`,
            `Response size: ${result.response_size ?? 0} bytes`,
            `Extracted data:\n${extractedData}`,
            result.error ? `Error: ${result.error}` : ""
        ].filter(Boolean);

        card.textContent = details.join("\n");
        card.style.whiteSpace = "pre-wrap";

        container.appendChild(card);
    });
}
