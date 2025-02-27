class ShoppingCart {
    constructor() {
        this.items = [];
        this.discountCode = null;
    }

    // Add an item to the cart
    addItem(name, price, quantity = 1) {
        let existingItem = this.items.find(item => item.name === name);
        if (existingItem) {
            existingItem.quantity += quantity;
        } else {
            this.items.push({ name, price, quantity });
        }
        console.log(`Added ${quantity} ${name}(s) to cart.`);
    }

    // Remove an item from the cart
    removeItem(name) {
        this.items = this.items.filter(item => item.name !== name);
        console.log(`Removed ${name} from cart.`);
    }

    // Update quantity of an item
    updateQuantity(name, quantity) {
        let item = this.items.find(item => item.name === name);
        if (item) {
            if (quantity > 0) {
                item.quantity = quantity;
                console.log(`Updated ${name} quantity to ${quantity}.`);
            } else {
                this.removeItem(name);
            }
        } else {
            console.log(`${name} not found in cart.`);
        }
    }

    // Apply a discount code
    applyDiscount(code) {
        const discounts = {
            "SAVE10": 0.10,
            "HOLIDAY20": 0.20,
            "FREESHIP": 0
        };

        if (code in discounts) {
            this.discountCode = code;
            console.log(`Discount code "${code}" applied.`);
        } else {
            console.log("Invalid discount code.");
        }
    }

    // Calculate total price
    calculateTotal() {
        let total = this.items.reduce((sum, item) => sum + (item.price * item.quantity), 0);

        if (this.discountCode && this.discountCode !== "FREESHIP") {
            let discountAmount = total * discounts[this.discountCode];
            total -= discountAmount;
            console.log(`Discount applied: -$${discountAmount.toFixed(2)}`);
        }

        return total.toFixed(2);
    }

    // Checkout function
    checkout() {
        if (this.items.length === 0) {
            console.log("Your cart is empty. Add items before checkout.");
            return;
        }

        let total = this.calculateTotal();
        console.log(`Checkout successful! Total amount: $${total}`);
        console.log("Thank you for shopping with us!");

        // Clear cart after checkout
        this.items = [];
        this.discountCode = null;
    }

    // Show cart items
    showCart() {
        if (this.items.length === 0) {
            console.log("Your cart is empty.");
            return;
        }
        console.log("Shopping Cart:");
        this.items.forEach(item => {
            console.log(`- ${item.name} x${item.quantity} ($${item.price} each)`);
        });
        console.log(`Total: $${this.calculateTotal()}`);
    }
}

// Example Usage:
const cart = new ShoppingCart();
cart.addItem("Laptop", 999.99, 1);
cart.addItem("Headphones", 49.99, 2);
cart.showCart();
cart.applyDiscount("SAVE10");
cart.showCart();
cart.checkout();
