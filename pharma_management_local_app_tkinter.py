import tkinter as tk
from tkinter import ttk, messagebox
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime

# MongoDB setup
url = "mongodb+srv://Srikanth_Saravanan:qwertyuiop@hospital.yzfdf9b.mongodb.net/?retryWrites=true&w=majority&appName=hospital"
client = MongoClient(url, server_api=ServerApi(version="1", strict=True, deprecation_errors=True))

try:
    client.admin.command('ping')
    print("Successfully connected to MongoDB!")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    messagebox.showerror("Connection Error", f"Error connecting to MongoDB: {e}")
    exit()

db = client['pharmacy']

# Function to add a product
def add_product(collection_name, data):
    collection = db[collection_name]
    collection.insert_one(data)

# Function to remove a product
def remove_product(collection_name, filter_data):
    collection = db[collection_name]
    result = collection.delete_one(filter_data)
    return result.deleted_count

# Function to get all products from a collection
def get_products(collection_name):
    collection = db[collection_name]
    return list(collection.find())

# Main application class
class PharmacyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Pharmacy Management System")
        self.geometry("800x600")

        self.collection_name = tk.StringVar(value="tablets")
        
        # Tabs for different product types
        self.create_tabs()

    def create_tabs(self):
        tab_frame = tk.Frame(self)
        tab_frame.pack(side=tk.TOP, fill=tk.X)
        
        tablet_tab = tk.Button(tab_frame, text="Tablets", command=lambda: self.load_tab("tablets"))
        capsule_tab = tk.Button(tab_frame, text="Capsules", command=lambda: self.load_tab("capsules"))
        syrup_tab = tk.Button(tab_frame, text="Syrups", command=lambda: self.load_tab("syrups"))
        other_items_tab = tk.Button(tab_frame, text="Other Items", command=lambda: self.load_tab("other_items"))

        tablet_tab.pack(side=tk.LEFT)
        capsule_tab.pack(side=tk.LEFT)
        syrup_tab.pack(side=tk.LEFT)
        other_items_tab.pack(side=tk.LEFT)

        self.content_frame = tk.Frame(self)
        self.content_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.load_tab("tablets")

    def load_tab(self, collection_name):
        self.collection_name.set(collection_name)

        for widget in self.content_frame.winfo_children():
            widget.destroy()

        add_product_frame = tk.LabelFrame(self.content_frame, text="Add a New Product")
        add_product_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        self.create_add_product_form(add_product_frame)

        display_products_frame = tk.LabelFrame(self.content_frame, text="Products in Stock")
        display_products_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.create_display_products_section(display_products_frame)

        remove_product_frame = tk.LabelFrame(self.content_frame, text="Remove a Product")
        remove_product_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        self.create_remove_product_form(remove_product_frame)

    def create_add_product_form(self, frame):
        tk.Label(frame, text="Product Name").grid(row=0, column=0, padx=5, pady=5)
        name_entry = tk.Entry(frame)
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="Brand").grid(row=1, column=0, padx=5, pady=5)
        brand_entry = tk.Entry(frame)
        brand_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame, text="Dosage").grid(row=2, column=0, padx=5, pady=5)
        dosage_entry = tk.Entry(frame)
        dosage_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(frame, text="Form").grid(row=3, column=0, padx=5, pady=5)
        form_entry = tk.Entry(frame)
        form_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(frame, text="Price").grid(row=4, column=0, padx=5, pady=5)
        price_entry = tk.Entry(frame)
        price_entry.grid(row=4, column=1, padx=5, pady=5)

        tk.Label(frame, text="Stock").grid(row=5, column=0, padx=5, pady=5)
        stock_entry = tk.Entry(frame)
        stock_entry.grid(row=5, column=1, padx=5, pady=5)

        tk.Label(frame, text="Expiry Date (YYYY-MM-DD)").grid(row=6, column=0, padx=5, pady=5)
        expiry_date_entry = tk.Entry(frame)
        expiry_date_entry.grid(row=6, column=1, padx=5, pady=5)

        def on_add_product():
            name = name_entry.get()
            brand = brand_entry.get()
            dosage = dosage_entry.get()
            form = form_entry.get()
            price = float(price_entry.get())
            stock = int(stock_entry.get())
            expiry_date = expiry_date_entry.get()

            if name and brand and dosage and form and price and stock and expiry_date:
                try:
                    expiry_date = datetime.strptime(expiry_date, "%Y-%m-%d")
                    product_data = {
                        "name": name,
                        "brand": brand,
                        "dosage": dosage,
                        "form": form,
                        "price": price,
                        "stock": stock,
                        "expiry_date": expiry_date,
                        "added_date": datetime.now()
                    }
                    add_product(self.collection_name.get(), product_data)
                    messagebox.showinfo("Success", f"Product {name} added successfully")
                except Exception as e:
                    messagebox.showerror("Error", f"Error adding product: {e}")
            else:
                messagebox.showerror("Input Error", "Please fill in all fields")

        add_button = tk.Button(frame, text="Add Product", command=on_add_product)
        add_button.grid(row=7, column=0, columnspan=2, pady=10)

    def create_display_products_section(self, frame):
        columns = ["Name", "Brand", "Dosage", "Form", "Price", "Stock", "Expiry Date", "Added Date"]
        product_tree = ttk.Treeview(frame, columns=columns, show="headings")
        for col in columns:
            product_tree.heading(col, text=col)
        product_tree.pack(fill=tk.BOTH, expand=True)

        products = get_products(self.collection_name.get())
        for product in products:
            product_tree.insert("", tk.END, values=(
                product["name"], product["brand"], product["dosage"], product["form"],
                product["price"], product["stock"], product["expiry_date"].strftime('%Y-%m-%d'),
                product["added_date"].strftime('%Y-%m-%d %H:%M:%S')
            ))

    def create_remove_product_form(self, frame):
        tk.Label(frame, text="Name of the product to remove").grid(row=0, column=0, padx=5, pady=5)
        remove_name_entry = tk.Entry(frame)
        remove_name_entry.grid(row=0, column=1, padx=5, pady=5)

        def on_remove_product():
            remove_name = remove_name_entry.get()
            if remove_name:
                deleted_count = remove_product(self.collection_name.get(), {"name": remove_name})
                if deleted_count > 0:
                    messagebox.showinfo("Success", f"Product {remove_name} removed successfully")
                else:
                    messagebox.showerror("Error", f"Product {remove_name} not found")
            else:
                messagebox.showerror("Input Error", "Please enter the name of the product to remove")

        remove_button = tk.Button(frame, text="Remove Product", command=on_remove_product)
        remove_button.grid(row=1, column=0, columnspan=2, pady=10)

if __name__ == "__main__":
    app = PharmacyApp()
    app.mainloop()

