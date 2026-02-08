async function testEndpoint() {
  const payload = {
    endpoint_url: document.getElementById("endpoint").value,
    api_key: document.getElementById("apikey").value,
    message: document.getElementById("message").value,
    audio_url: document.getElementById("audio").value
  };

  const response = await fetch("http://127.0.0.1:8000/test-endpoint", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-API-Key": "test123"
    },
    body: JSON.stringify(payload)
  });

  document.getElementById("output").textContent =
    JSON.stringify(await response.json(), null, 2);
}
