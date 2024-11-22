import datetime
import os
import json

class VendingMachine:
    def __init__(self):
        self.log_file = "vending_machine_log.txt"
        self.inventory_file = "inventory.json"  # store inventory in a JSON file
        self.items = []  # inventory list will be loaded from the file
        self.balance = 0.0
        self.load_inventory()  # load inventory from file

    def load_inventory(self):
        if os.path.exists(self.inventory_file):
            with open(self.inventory_file, "r") as file:
                self.items = json.load(file)  # load items from JSON file
        else:
            # If no inventory file exists, raise an error 
            print(f"Error: {self.inventory_file} not found! Please make sure the inventory file exists.")
            exit(1) 

    def save_inventory(self):
        # Save the current inventory to the JSON file
        with open(self.inventory_file, "w") as file:
            json.dump(self.items, file, indent=4)

    def display_items(self):
        # Show available items, prices, and stock counts with updated stock
        print("Items available:")
        for index, item in enumerate(self.items, start=1):
            print(f"{index}. {item['name']}: ${item['price']:.2f} (Stock: {item['stock']})")

    def insert_money(self):
        # User inserts money
        while True:
            try:
                amount = float(input("Insert money (enter the amount in dollars): $"))
                if amount <= 0:
                    print("Please insert a valid amount of money.")
                else:
                    self.balance += amount
                    print(f"Current balance: ${self.balance:.2f}")
                    break
            except ValueError:
                print("Invalid input. Please enter a number.")

    def log_purchase(self, item_name, item_price, item_stock, balance_before, balance_after):
        # Log the transaction to a file with timestamp
        with open(self.log_file, "a") as log_file:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = (
                f"{timestamp} - Purchased {item_name} for ${item_price:.2f}. "
                f"Balance before: ${balance_before:.2f}, Balance after: ${balance_after:.2f}. "
                f"Remaining stock: {item_stock}\n"
            )
            log_file.write(log_entry)

    def initialize_log(self):
        # Initialize log file with header if it doesn't exist
        if not os.path.exists(self.log_file):
            with open(self.log_file, "w") as log_file:
                log_file.write("Vending Machine Transaction Log\n")

    def purchase_item(self):
        # User selects an item to purchase by number
        while True:
            self.display_items()  # Display updated stock
            try:
                item_choice = int(input("\nEnter the number of the item you'd like to purchase or '0' to quit: "))
                
                if item_choice == 0:
                    print("Thank you for using the vending machine!")
                    break

                if 1 <= item_choice <= len(self.items):
                    item = self.items[item_choice - 1]
                    item_name = item["name"]
                    item_price = item["price"]
                    item_stock = item["stock"]

                    if item_stock > 0:
                        if self.balance >= item_price:
                            # Log the purchase details before the transaction
                            balance_before = self.balance
                            self.balance -= item_price
                            item["stock"] -= 1  # update stock after purchase
                            balance_after = self.balance
                            print(f"Dispensing {item_name}... Enjoy! Remaining balance: ${self.balance:.2f}")
                            
                            # Log the transaction with updated stock count
                            self.log_purchase(item_name, item_price, item["stock"], balance_before, balance_after)
                            # Save updated inventory to file
                            self.save_inventory()
                        else:
                            print(f"Insufficient funds. {item_name} costs ${item_price:.2f}. Please insert more money.")
                            self.insert_money()
                    else:
                        print(f"Sorry, {item_name} is out of stock.")

                else:
                    print("Invalid item number. Please choose a valid item number.")
            except ValueError:
                print("Invalid input. Please enter a number.")

            # Ask if the user wants to continue or exit
            continue_choice = input("Would you like to purchase another item? (y/n): ").lower()
            if continue_choice != 'y':
                print("Thank you for using the vending machine!")
                break

if __name__ == "__main__":
    vending_machine = VendingMachine()
    print("Welcome to the Vending Machine!")

    # Initialize log file with a header
    vending_machine.initialize_log()

    while True:
        vending_machine.insert_money()
        vending_machine.purchase_item()
        break
