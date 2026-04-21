# 🧪 DoughBot Enhancement Test Cases

## Test Scenarios & Expected Outputs

### ✅ Test 1: Price Check
**User Input:** `"What's the price of croissant?"`

**Expected Response:**
```
💰 **Croissant** costs **PHP 120**. Fresh and delicious!
```

---

### ✅ Test 2: Multiple Price Items
**User Input:** `"How much do your coffees cost?"`

**Expected Response:**
```
📋 **Price Check Results:**
- ☕ Espresso: **PHP 90**
- Americano: **PHP 100**
- ☕ Cappuccino: **PHP 120**
- ☕ Latte: **PHP 130**
- Mocha: **PHP 140**
```

---

### ✅ Test 3: Stock Status - Single Item
**User Input:** `"Is croissant in stock?"`

**Expected Response:**
```
✅ **Croissant** - In Stock
📊 Available: 45 units
```

---

### ✅ Test 4: Stock Status - Low Stock Warning
**User Input:** `"What about Danish?"`

**Expected Response:**
```
⚠️ **Danish** - Low Stock
📊 Available: 8 units
```

---

### ✅ Test 5: Stock Status - Multiple Items
**User Input:** `"Check stock for breads"`

**Expected Response:**
```
📦 **Stock Status Check:**
✅ 🥐 Croissant: In Stock (45 units)
✅ 🍞 Baguette: In Stock (32 units)
✅ 🥖 Brioche: In Stock (28 units)
⚠️ 🥯 Pain au Chocolat: Low Stock (15 units)
✅ Fougasse: In Stock (22 units)
```

---

### ✅ Test 6: Best Pairing - Specific Item
**User Input:** `"What goes with croissant?"`

**Expected Response:**
```
✨ **Best Pairing for Croissant:**

🥐 **Croissant** + ☕ **Latte**

💭 The buttery, flaky croissant pairs perfectly with smooth, 
   creamy latte for a balanced breakfast.

🎯 Perfect for: **Classic Morning Enthusiast**

Want to order this combo?
```

---

### ✅ Test 7: Best Pairing - Brioche
**User Input:** `"What should I pair with brioche?"`

**Expected Response:**
```
✨ **Best Pairing for Brioche:**

🥐 **Brioche** + ☕ **Cappuccino**

💭 Rich, sweet brioche complements the bold espresso and 
   velvety foam of cappuccino beautifully.

🎯 Perfect for: **Coffee Lover's Choice**

Want to order this combo?
```

---

### ✅ Test 8: Random Pairing (No Item Specified)
**User Input:** `"Recommend a pairing"`

**Expected Response (Random):**
```
✨ **Best Pairing Suggestion:**

Sourdough + ☕ Flat White

💭 Tangy sourdough balances perfectly with smooth, velvety 
   flat white espresso.

🎯 Perfect for: **Artisan Appreciator**
```

---

### ✅ Test 9: Order Guidance
**User Input:** `"How do I order?"`

**Expected Response (Random Persona):**
```
🛍️ **Order Guidance - Find Your Perfect Match!**

**☀️ Morning Enthusiast**
→ Croissant + Latte - Start your day right!

For those who love a balanced, smooth breakfast combo

**Steps to Order:**
1. Choose your item from the menu
2. Check our stock status
3. Add to cart with quantity
4. Choose payment method (GCash, Maya, or Cash)
5. Proceed to checkout - get PHP 300 signup bonus! 💳

Which combo sounds good to you?
```

---

### ✅ Test 10: All Features Combined
**User Input:** `"Is sourdough in stock? What coffee should I pair it with? How do I order?"`

**Expected Response (Sequential):**
```
Step 1 - Stock Check:
✅ **Sourdough** - In Stock
📊 Available: 18 units

Step 2 - Pairing:
✨ **Best Pairing for Sourdough:**
🥐 **Sourdough** + ☕ **Flat White**
💭 Tangy sourdough balances perfectly with smooth, velvety flat white espresso.
🎯 Perfect for: **Artisan Appreciator**

Step 3 - Order Guidance:
🛍️ **Order Guidance - Find Your Perfect Match!**
[Shows appropriate persona with ordering steps]
```

---

## 🎯 Integration Test Cases

### Test A: Keyword Detection
**Input:** `"price check on latte"`
- Should trigger: Price Check handler
- Match: "latte" → "☕ Latte": PHP 130

### Test B: Synonym Detection  
**Input:** `"what's available"`
- Should trigger: Stock Status handler
- Shows all in-stock items

### Test C: Pairing Variations
**Input:** `"what pairs best with croissant?"`
- Should trigger: Best Pairing handler
- Match: "croissant" → Latte pairing

### Test D: Order Process
**Input:** `"help me buy something"`
- Should trigger: Order Guidance handler
- Shows persona-based recommendation

---

## 💡 Edge Cases

### Case 1: Item Not Found
**Input:** `"What's the price of pizza?"`

**Expected Response:**
```
I didn't find that item. Try asking about: Croissant, Baguette, 
Brioche, Coffee, Latte, Cappuccino, etc.
```

### Case 2: Ambiguous Query
**Input:** `"What about latte?"`
- If after "price" context → Price check
- If after "pairing" context → Stock status
- Otherwise → General response

### Case 3: Multiple Matches
**Input:** `"prices"`
- Should show all items with prices
- Formatted as price list

---

## 📋 Persona Variation Test

Run multiple order guidance queries to see all 5 personas:

1. **☀️ Morning Enthusiast** (Croissant + Latte)
2. **💪 Energy Booster** (Espresso + Pain au Chocolat)
3. **🎨 Flavor Explorer** (Sourdough + Flat White)
4. **🍫 Sweet Tooth** (Danish + Mocha)
5. **🌙 Evening Sipper** (Fougasse + Macchiato)

Each persona appears randomly with appropriate recommendations.

---

## 🔍 Testing Checklist

- [ ] Price check returns correct PHP amounts
- [ ] Stock status shows units and warnings
- [ ] Pairing suggestions include persona descriptions
- [ ] Order guidance displays 5 different personas
- [ ] Emoji indicators appear in all responses
- [ ] Item matching works with partial names
- [ ] Low stock items show ⚠️ warning
- [ ] Available items show ✅ indicator
- [ ] Coffee items always show available (999 units)
- [ ] Response formatting is clean and readable

---

## 🚀 How to Test

1. **Run the Streamlit app:**
   ```bash
   streamlit run chatbot.py
   ```

2. **Test each scenario above in the chat**

3. **Verify responses match expected output**

4. **Check for proper emoji usage and formatting**

5. **Test edge cases and error handling**

---

**Last Updated:** April 2026
**Test Status:** Ready for QA ✅
