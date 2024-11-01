document.getElementById("urlForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const urlInput = document.getElementById("url");
  const loadingDiv = document.getElementById("loading");
  const resultDiv = document.getElementById("result");
  const responseDiv = document.getElementById("response");
  const errorDiv = document.getElementById("error");

  // Reset state
  loadingDiv.classList.remove("hidden");
  resultDiv.classList.add("hidden");
  errorDiv.classList.add("hidden");

  try {
    /**
     * Sends a POST request to the "/generate" endpoint with the URL input value.
     *
     * @returns {Promise<Response>} The response from the fetch request.
     */
    const response = await fetch("/generate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        url: urlInput.value,
      }),
    });

    const data = await response.json();

    if (data.status === "success") {
      responseDiv.textContent = data.response;
      resultDiv.classList.remove("hidden");
    } else {
      errorDiv.textContent =
        data.error || "An error occurred. Please try again.";
      errorDiv.classList.remove("hidden");
    }
  } catch (error) {
    errorDiv.textContent = "An error occurred. Please try again.";
    errorDiv.classList.remove("hidden");
  } finally {
    loadingDiv.classList.add("hidden");
  }
});
