// Simplified payment.js - Handles NSS donation form

document.addEventListener("DOMContentLoaded", function () {
  // Select form elements
  const donationForm = document.querySelector(".form")
  const nameInput = document.querySelector(
    'input[placeholder="Enter your name"]'
  )
  const phoneInput = document.querySelector(
    'input[placeholder="Enter 10-digit mobile number"]'
  )
  const amountInput = document.querySelector('input[type="number"]')
  const amountButtons = document.querySelectorAll(".amount-btn")
  const payButton = document.querySelector(".btn-pay")

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
    const phone = phoneInput.value.trim()
    const amount = amountInput.value.trim()

    if (!name) {
      alert("Please enter your name")
      return
    }

    if (!phone || phone.length !== 10 || !/^\d+$/.test(phone)) {
      alert("Please enter a valid 10-digit phone number")
      return
    }

    if (!amount || amount <= 0) {
      alert("Please enter a valid amount")
      return
    }

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
        phoneNumber: phone,
        amount: parseFloat(amount),
      }),
    })
      .then((response) => response.json())
      .then((data) => {
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
        alert("Payment failed. Please try again.")
      })
    //   .finally(() => {
    //     // Reset button state
    //     payButton.innerHTML = originalButtonHTML
    //     payButton.disabled = false
    //   })
  })
})
