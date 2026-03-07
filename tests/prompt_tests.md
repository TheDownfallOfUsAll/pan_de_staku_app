# DoughBot Prompt Tests

This file contains prompt tests for smarter DoughBot behavior.

---

# Test Case 1 - Greeting

### User Input
Hello

### Expected Output
One friendly greeting variant, for example:
- "Bonjour! I am DoughBot. Looking for bread, coffee, or a combo today?"
- "Welcome to Pan de Staku. I can suggest items, prices, and pairings."
- "Hi! Ask me for recommendations, menu details, or order help."

---

# Test Case 2 - Full Menu

### User Input
Show me your menu

### Expected Output
Returns a list of all menu items from `all_menu`.

---

# Test Case 3 - Bread List

### User Input
What breads do you have?

### Expected Output
Returns bread-only items:
- Croissant
- Baguette
- Brioche
- Pain au Chocolat
- Fougasse
- Sourdough
- Danish

---

# Test Case 4 - Coffee List

### User Input
What coffee do you serve?

### Expected Output
Returns coffee-only items from `coffee_menu`.

---

# Test Case 5 - Recommendation (Varied)

### User Input
Can you recommend something?

### Expected Output
Returns one combo recommendation, such as:
- Croissant with Latte
- Brioche with Cappuccino
- Pain au Chocolat with Mocha
- Sourdough with Flat White

---

# Test Case 6 - Item Price

### User Input
Price of brioche

### Expected Output
`Brioche is PHP 150.`

---

# Test Case 7 - Item Pairing

### User Input
What goes with croissant?

### Expected Output
`Croissant pairs well with Latte.`

---

# Test Case 8 - Delivery

### User Input
Do you offer delivery?

### Expected Output
A delivery response with PHP 40 base fee.

---

# Test Case 9 - Payment Guidance

### User Input
How do I pay?

### Expected Output
Mentions:
- GCash and Maya
- 11-digit mobile number
- 6-digit OTP

---

# Test Case 10 - Branches

### User Input
What branches are available?

### Expected Output
`Branches are available in Manila, Cebu, and Davao.`

---

# Test Case 11 - Order Steps

### User Input
How can I order?

### Expected Output
Mentions flow:
1. Login
2. Order page
3. Add to cart
4. Checkout in Cart

---

# Test Case 12 - Follow-up Context

### User Input
I want brioche  
How much is it?

### Expected Output
Second prompt should use context (`it`) and return:
`Brioche is PHP 150.`

---

# Test Case 13 - Unknown Prompt

### User Input
Tell me a joke about rockets

### Expected Output
Fallback guidance listing supported topics:
- menu
- prices
- pairings
- delivery
- payment
- branches
- order steps
