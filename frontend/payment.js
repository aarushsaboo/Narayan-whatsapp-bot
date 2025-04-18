// NSS Donation Form JavaScript with country code support
document.addEventListener("DOMContentLoaded", function () {
  // Select form elements
  const nameInput = document.getElementById("name-input")
  const countryCodeSelect = document.getElementById("country-code")
  const phoneInput = document.getElementById("phone-input")
  const amountInput = document.getElementById("amount-input")
  const amountButtons = document.querySelectorAll(".amount-btn")
  const payButton = document.getElementById("pay-button")

  // Set up amount buttons
  amountButtons.forEach((button) => {
    button.addEventListener("click", function () {
      amountButtons.forEach((btn) => btn.classList.remove("active"))
      this.classList.add("active")
      amountInput.value = this.textContent.replace("₹", "")
    })
  })

  // Handle payment submission
  payButton.addEventListener("click", function () {
    // Basic validation
    const name = nameInput.value.trim()
    const countryCode = countryCodeSelect.value
    const phone = phoneInput.value.trim()
    const amount = amountInput.value.trim()

    if (!name) {
      alert("Please enter your name")
      return
    }

    if (!phone || !/^\d+$/.test(phone)) {
      alert("Please enter a valid phone number")
      return
    }

    if (!amount || amount <= 0) {
      alert("Please enter a valid amount")
      return
    }

    // Format full phone number with country code
    const fullPhoneNumber = countryCode + phone

    // Show loading state
    const originalButtonHTML = payButton.innerHTML
    // payButton.innerHTML = "<span>Processing...</span>"
    // payButton.disabled = true

    // Send payment data to backend
    fetch("http://localhost:4000/payment", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        name: name,
        phoneNumber: fullPhoneNumber,
        amount: parseFloat(amount),
      }),
    })
      .then((response) => {
        if (!response.ok) throw new Error("Network response was not ok")
        return response.text()
      })
      .then((twiml) => {
        // Handle success
        alert("Thank you for your donation of ₹" + amount + "!")

        // Reset form
        // nameInput.value = ""
        // phoneInput.value = ""
        // amountInput.value = ""
        // amountButtons.forEach((btn) => btn.classList.remove("active"))
      })
      .catch((error) => {
        // Handle error
        console.error("Payment error:", error)
        alert("Payment failed. Please try again.")
      })
      .finally(() => {
        // Reset button state
        // payButton.innerHTML = originalButtonHTML
        // payButton.disabled = false
      })
  })
})
