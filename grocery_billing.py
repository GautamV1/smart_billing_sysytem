import datetime
import csv

# ==== Load inventory from CSV ====
def load_inventory(filename):
    inventory = {}
    try:
        with open(filename, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                item = row['Item'].strip()
                price = float(row['Price'])
                stock = int(row['Stock'])  # corrected
                inventory[item] = {'Price': price, 'Stock': stock}
    except FileNotFoundError:
        print(f"Error: '{filename}' not found.")
    except Exception as e:
        print(f"Error loading inventory: {e}")
    return inventory

# === Display inventory ===
def display_inventory(inventory):
    print("\nAvailable items:")
    print("{:<15} {:<10} {:<10}".format("Item", "Price", "Stock"))
    print("-" * 35)
    for item, details in inventory.items():
        print("{:<15} Rs{:<9.2f} {:<10}".format(item, details['Price'], details['Stock']))

# ==== Initialize ====
inventory = load_inventory("inventory.csv")
cart = []

# === Add item to cart ===
def add_item():
    display_inventory(inventory)
    name = input("Enter item name: ").strip()

    if name not in inventory:
        print("Item not found in inventory.\n")
        return

    try:
        qty = int(input("Enter quantity: "))
    except ValueError:
        print("Invalid quantity.\n")
        return

    if qty <= 0 or qty > inventory[name]['Stock']:
        print("Invalid quantity. Either zero or exceeds stock.\n")
        return

    price = inventory[name]['Price']
    inventory[name]['Stock'] -= qty  # Deduct stock
    cart.append({'name': name, 'qty': qty, 'price': price})
    print(f"Added {qty} x {name} to cart.\n")

# === View cart ===
def view_cart():
    if not cart:
        print("Cart is empty.\n")
        return 0

    print("\nYour Cart:")
    print("-" * 40)
    total = 0
    for item in cart:
        subtotal = item['qty'] * item['price']
        print(f"{item['name']} - {item['qty']} x Rs{item['price']} = Rs{subtotal:.2f}")
        total += subtotal
    print("-" * 40)
    print(f"Subtotal: Rs{total:.2f}")
    return total

# === Generate bill and save as .txt ===
def generate_bill():
    if not cart:
        print("Cart is empty. Please add items first.\n")
        return

    total = view_cart()
    gst = total * 0.05
    grand_total = total + gst

    print(f"GST (5%): Rs{gst:.2f}")
    print(f"Total Payable: Rs{grand_total:.2f}")

    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"bill_{timestamp}.txt"

    with open(filename, 'w') as f:
        f.write("Royal Grocery Store Invoice\n")
        f.write(f"Date: {datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}\n")
        f.write("-" * 40 + "\n")
        for item in cart:
            line = f"{item['name']} - {item['qty']} x Rs{item['price']} = Rs{item['qty'] * item['price']:.2f}\n"
            f.write(line)
        f.write("-" * 40 + "\n")
        f.write(f"Subtotal: Rs{total:.2f}\n")
        f.write(f"GST (5%): Rs{gst:.2f}\n")
        f.write(f"Total Payable: Rs{grand_total:.2f}\n")
        f.write("-" * 40 + "\n")
        f.write("Thank you for shopping with us!\n")

    print(f"Bill saved as: {filename}\n")

# === Main Menu ===
def main():
    while True:
        print("\nGrocery Billing Menu:")
        print("1. Add item")
        print("2. View cart")
        print("3. Generate bill")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ").strip()

        if choice == '1':
            add_item()
        elif choice == '2':
            view_cart()
        elif choice == '3':
            generate_bill()
        elif choice == '4':
            print("Exiting... Thank you!")
            break
        else:
            print("Invalid choice. Please enter 1-4.\n")

# === Entry Point ===
if __name__ == "__main__":
    main()
