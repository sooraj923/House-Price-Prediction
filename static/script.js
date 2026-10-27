const form = document.getElementById("prediction-form");
const submitButton = document.getElementById("submit-button");
const resultEmpty = document.getElementById("result-empty");
const resultSuccess = document.getElementById("result-success");
const resultError = document.getElementById("result-error");
const bathInput = document.getElementById("bath");

document.querySelectorAll(".bath-option").forEach((button) => {
  button.addEventListener("click", () => {
    document.querySelectorAll(".bath-option").forEach((item) => item.classList.remove("active"));
    button.classList.add("active");
    bathInput.value = button.dataset.bath;
  });
});

function showError(message) {
  resultEmpty.classList.add("hidden");
  resultSuccess.classList.add("hidden");
  resultError.textContent = message;
  resultError.classList.remove("hidden");
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  resultError.classList.add("hidden");

  const payload = {
    location: document.getElementById("location").value.trim(),
    total_sqft: Number(document.getElementById("total_sqft").value),
    bedrooms: Number(document.getElementById("bedrooms").value),
    bath: Number(bathInput.value)
  };

  if (!payload.location || !Number.isFinite(payload.total_sqft) || payload.total_sqft <= 0) {
    showError("Please enter a location and a valid area greater than zero.");
    return;
  }

  submitButton.disabled = true;
  submitButton.querySelector("span:first-child").textContent = "Calculating estimate…";

  try {
    const response = await fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || data.details || "Unable to calculate a prediction.");
    }

    document.getElementById("price-value").textContent =
      Number(data.predicted_price_lakhs).toLocaleString("en-IN", {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      });
    document.getElementById("result-location").textContent = payload.location;
    document.getElementById("result-area").textContent =
      `${payload.total_sqft.toLocaleString("en-IN")} sq. ft.`;
    document.getElementById("result-config").textContent =
      `${payload.bedrooms} bed · ${payload.bath} bath`;

    resultEmpty.classList.add("hidden");
    resultError.classList.add("hidden");
    resultSuccess.classList.remove("hidden");
  } catch (error) {
    showError(error.message || "Something went wrong. Please try again.");
  } finally {
    submitButton.disabled = false;
    submitButton.querySelector("span:first-child").textContent = "Estimate my home price";
  }
});

document.getElementById("reset-button").addEventListener("click", () => {
  resultSuccess.classList.add("hidden");
  resultError.classList.add("hidden");
  resultEmpty.classList.remove("hidden");
  document.getElementById("location").focus();
});
