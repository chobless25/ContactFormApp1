import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
import re

# Validate email format
def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

# Validate phone number (digits only and length between 7–15)
def is_valid_phone(phone):
    return phone.isdigit() and 7 <= len(phone) <= 15

def save_contact():
    name = entry_name.get()
    email = entry_email.get()
    phone = entry_phone.get()
    message = text_msg.get("1.0", tk.END).strip()

    if not(name and email and phone and message):
        messagebox.showerror("Error", "All fields are required")
        return
    if not is_valid_email(email):
        messagebox.showerror("Error", "Invalid email format")
        return
    if not is_valid_phone(phone):
        messagebox.showerror("Error", "Invalid phone number")
        return

    file_exists = os.path.isfile('contacts.csv')
    with open('contacts.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Name", "Email", "Phone", "Message"])
        writer.writerow([name, email, phone, message])

    messagebox.showinfo("Success", "Contact saved successfully!")
    clear_fields()

def clear_fields():
    entry_name.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_phone.delete(0, tk.END)
    text_msg.delete("1.0", tk.END)

def view_contacts():
    if not os.path.isfile('contacts.csv'):
        messagebox.showinfo("No Data", "No contacts found yet!")
        return

    top = tk.Toplevel(root)
    top.title("Saved Contacts")
    top.geometry("600x400")

    tree = ttk.Treeview(top, columns=("Name", "Email", "Phone", "Message"), show="headings")
    tree.heading("Name", text="Name")
    tree.heading("Email", text="Email")
    tree.heading("Phone", text="Phone")
    tree.heading("Message", text="Message")
    tree.pack(fill=tk.BOTH, expand=True)

    with open('contacts.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # skip header
        for row in reader:
            tree.insert("", tk.END, values=row)

# GUI layout
root = tk.Tk()
root.title("Contact Form")
root.geometry("400x500")
root.resizable(False,False)

tk.Label(root, text="Contact Form", font=("Arial", 18, "bold")).pack(pady=10)

tk.Label(root, text="Name:").pack(anchor="w", padx=20)
entry_name = tk.Entry(root, width=40)
entry_name.pack(padx=20, pady=5)

tk.Label(root, text="Email:").pack(anchor="w", padx=20)
entry_email = tk.Entry(root, width=40)
entry_email.pack(padx=20, pady=5)

tk.Label(root, text="Phone:").pack(anchor="w", padx=20)
entry_phone = tk.Entry(root, width=40)
entry_phone.pack(padx=20, pady=5)

tk.Label(root, text="Message:").pack(anchor="w", padx=20)
text_msg = tk.Text(root, width=30, height=5)
text_msg.pack(padx=20, pady=5)

tk.Button(root, text="Submit", bg="#4CAF50", fg="white", command=save_contact, width=15).pack(pady=10)
tk.Button(root, text="View Contacts", bg="#2196F3", fg="white", command=view_contacts, width=15).pack(pady=5)

root.mainloop()
