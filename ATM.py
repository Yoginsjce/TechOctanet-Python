import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk

class ATMMachine:
    def __init__(self, initial_balance=0, initial_pin="1234"):
        self.balance = initial_balance
        self.pin = initial_pin
        self.transaction_history = []

    def check_balance(self):
        return self.balance

    def withdraw_cash(self, amount):
        if amount > self.balance:
            return "Insufficient balance."
        elif amount <= 0:
            return "Invalid amount entered."
        else:
            self.balance -= amount
            self.transaction_history.append(f"Withdrawal: ${amount}")
            return f"${amount} has been withdrawn."

    def deposit_cash(self, amount):
        if amount <= 0:
            return "Invalid amount entered."
        self.balance += amount
        self.transaction_history.append(f"Deposit: ${amount}")
        return f"${amount} has been deposited."

    def change_pin(self, old_pin, new_pin):
        if old_pin == self.pin:
            if len(new_pin) == 4 and new_pin.isdigit():
                self.pin = new_pin
                self.transaction_history.append("PIN changed successfully.")
                return "PIN has been successfully changed."
            else:
                return "New PIN must be a 4-digit number."
        else:
            return "Incorrect old PIN."

    def show_transaction_history(self):
        if not self.transaction_history:
            return "No transactions yet."
        return "\n".join(self.transaction_history)


class ATMApp:
    def __init__(self, root, atm_machine, bg_image_path):
        self.atm = atm_machine
        self.root = root
        self.root.title("ATM Machine")
        self.root.geometry("400x600")

        # Load and set background image
        self.bg_image = Image.open(bg_image_path)
        self.bg_image = self.bg_image.resize((400, 600), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self.root, text="Welcome to the ATM", font=("Helvetica", 18, "bold"), bg="#2e3d49", fg="white")
        self.label.pack(pady=20)

        self.pin_label = tk.Label(self.root, text="Enter PIN:", font=("Helvetica", 14), bg="#2e3d49", fg="white")
        self.pin_label.pack(pady=10)

        self.pin_entry = tk.Entry(self.root, show="*", font=("Helvetica", 16))
        self.pin_entry.pack(pady=10)

        self.pin_button = tk.Button(self.root, text="Enter PIN", command=self.enter_pin, font=("Helvetica", 14), bg="#4CAF50", fg="white", width=20)
        self.pin_button.pack(pady=10)

    def enter_pin(self):
        pin = self.pin_entry.get()
        if pin == self.atm.pin:
            self.label.config(text="Access Granted!")
            self.pin_entry.pack_forget()
            self.pin_button.pack_forget()
            self.create_transaction_buttons()
        else:
            self.label.config(text="Incorrect PIN. Try Again.")
            self.pin_entry.delete(0, tk.END)

    def create_transaction_buttons(self):
        self.buttons_frame = tk.Frame(self.root, bg="#2e3d49")
        self.buttons_frame.pack(pady=20)

        buttons = [
            ("Check Balance", self.check_balance),
            ("Withdraw Cash", self.withdraw_cash),
            ("Deposit Cash", self.deposit_cash),
            ("Change PIN", self.change_pin),
            ("Transaction History", self.show_transaction_history),
            ("Exit ATM", self.exit_atm),  # Exit ATM feature
        ]

        for i, (text, command) in enumerate(buttons):
            button = tk.Button(self.buttons_frame, text=text, command=command, font=("Helvetica", 14), bg="#FF5722", fg="white", width=20)
            button.grid(row=i, column=0, padx=10, pady=10)

    def check_balance(self):
        balance = self.atm.check_balance()
        messagebox.showinfo("Balance Inquiry", f"Your current balance is: ${balance}")

    def withdraw_cash(self):
        amount = self.get_amount_from_user("Enter amount to withdraw:")
        if amount is not None:
            message = self.atm.withdraw_cash(amount)
            messagebox.showinfo("Withdraw Cash", message)

    def deposit_cash(self):
        amount = self.get_amount_from_user("Enter amount to deposit:")
        if amount is not None:
            message = self.atm.deposit_cash(amount)
            messagebox.showinfo("Deposit Cash", message)

    def change_pin(self):
        old_pin = self.get_pin_from_user("Enter your current PIN:")
        if old_pin:
            if old_pin != self.atm.pin:
                messagebox.showerror("Change PIN", "The entered current PIN is incorrect.")
                return
            new_pin = self.get_pin_from_user("Enter a new 4-digit PIN:")
            if new_pin:
                message = self.atm.change_pin(old_pin, new_pin)
                messagebox.showinfo("Change PIN", message)

    def show_transaction_history(self):
        history = self.atm.show_transaction_history()
        messagebox.showinfo("Transaction History", history)

    def exit_atm(self):
        if messagebox.askyesno("Exit ATM", "Are you sure you want to exit?"):
            self.root.quit()

    def get_amount_from_user(self, prompt):
        try:
            amount = simpledialog.askfloat("Amount", prompt)
            if amount is None or amount <= 0:
                raise ValueError
            return amount
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid amount.")
            return None

    def get_pin_from_user(self, prompt):
        pin = simpledialog.askstring("PIN", prompt, show="*")
        if pin and pin.isdigit() and len(pin) == 4:
            return pin
        else:
            messagebox.showerror("Invalid PIN", "PIN must be a 4-digit number.")
            return None


if __name__ == "__main__":
    root = tk.Tk()
    atm_machine = ATMMachine(initial_balance=500)

    # Replace with the path to your downloaded background image
    bg_image_path = "atm image.jpg"
    app = ATMApp(root, atm_machine, bg_image_path)
    root.mainloop()
