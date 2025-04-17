// payment.js - Handles NSS donation form interactions and payment processing

document.addEventListener("DOMContentLoaded", function () {
  // Variables to store DOM elements
  const nameInput = document.querySelector(
    '.form-control[placeholder="Enter your name"]'
  )
  const phoneInput = document.querySelector(
    '.form-control[placeholder="Enter 10-digit mobile number"]'
  )
  const amountInput = document.querySelector('.form-control[type="number"]')
  const amountButtons = document.querySelectorAll(".amount-btn")
  const payButton = document.querySelector(".btn-pay")

  // Set up event listeners
  setupAmountButtons()
  setupPaymentSubmission()

  // Handle amount button selection
  function setupAmountButtons() {
    amountButtons.forEach((button) => {
      button.addEventListener("click", function () {
        // Remove active class from all buttons
        amountButtons.forEach((btn) => {
          btn.classList.remove("active")
        })

        // Add active class to clicked button
        this.classList.add("active")

        // Set the amount in the custom field
        const amount = this.textContent.replace("₹", "")
        amountInput.value = amount
      })
    })
  }

  // Handle payment submission
  function setupPaymentSubmission() {
    payButton.addEventListener("click", function () {
      // Get form values
      const name = nameInput.value.trim()
      const phone = phoneInput.value.trim()
      const amount = amountInput.value.trim()

      // Basic validation
      if (!validateForm(name, phone, amount)) {
        return
      }

      // Process payment
      processPayment(name, phone, amount)
    })
  }

  // Validate form fields
  function validateForm(name, phone, amount) {
    if (!name) {
      alert("Please enter your name")
      nameInput.focus()
      return false
    }

    if (!phone || phone.length !== 10 || !/^\d+$/.test(phone)) {
      alert("Please enter a valid 10-digit phone number")
      phoneInput.focus()
      return false
    }

    if (!amount || isNaN(parseFloat(amount)) || parseFloat(amount) <= 0) {
      alert("Please enter a valid amount")
      amountInput.focus()
      return false
    }

    return true
  }

  // Process payment by sending request to backend
  function processPayment(name, phone, amount) {
    // Show loading state
    const originalButtonHTML = payButton.innerHTML
    payButton.innerHTML = "<span>Processing...</span>"
    payButton.disabled = true

    // Create payment data object
    const paymentData = {
      name: name,
      phoneNumber: phone,
      amount: parseFloat(amount),
    }

    // Send request to backend
    fetch("http://localhost:4000/payment", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(paymentData),
    })
        .then((response) => {
          print(response)
        if (!response.ok) {
          throw new Error(
            "Payment request failed with status: " + response.status
          )
        }
        return response.json()
      })
      .then((data) => {
        // Handle successful response
          // handleSuccessfulPayment(data, amount)
        print("yay")
      })
      .catch((error) => {
        // Handle errors
        console.error("Error:", error)
        alert("Payment failed. Please try again.")
      })
      .finally(() => {
        // Reset button state
        payButton.innerHTML = originalButtonHTML
        payButton.disabled = false
      })
  }

  // Handle successful payment
  function handleSuccessfulPayment(responseData, amount) {
    // Display success message
    alert("Thank you for your donation of ₹" + amount + "!")

    // You can handle additional logic based on response data
    console.log("Payment successful:", responseData)

    // Reset the form
    resetForm()
  }

  // Reset form after submission
  function resetForm() {
    nameInput.value = ""
    phoneInput.value = ""
    amountInput.value = ""
    amountButtons.forEach((btn) => {
      btn.classList.remove("active")
    })
  }
})
