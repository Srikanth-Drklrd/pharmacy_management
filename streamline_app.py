import streamlit as st
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime, date
import pandas as pd

# MongoDB setup
url = "mongodb+srv://Srikanth_Saravanan:qwertyuiop@hospital.yzfdf9b.mongodb.net/?retryWrites=true&w=majority&appName=hospital"
client = MongoClient(url, server_api=ServerApi(version="1", strict=True, deprecation_errors=True))

try:
    client.admin.command('ping')
    st.success("Successfully connected to MongoDB!")
except Exception as e:
    st.error(f"Error connecting to MongoDB: {e}")

db = client['pharmacy']

def add_product(data, collection_name):
    collection = db[collection_name]
    collection.insert_one(data)

def remove_product(filter_data, collection_name):
    collection = db[collection_name]
    collection.delete_one(filter_data)

def get_products(collection_name=None):
    if collection_name and collection_name != "all":
        collection = db[collection_name]
        return list(collection.find())
    else:
        all_products = []
        for collection in st.session_state.collections[1:]:  # Skip 'all'
            products = db[collection].find()
            for product in products:
                product["collection"] = collection
                all_products.append(product)
        return all_products

def delete_collection(collection_name):
    db[collection_name].drop()

def create_collection(collection_name):
    db.create_collection(collection_name)

# Initialize session state for collections
if 'collections' not in st.session_state:
    st.session_state.collections = ["all"] + db.list_collection_names()

# Initialize session state for refreshing products
if 'refresh_products' not in st.session_state:
    st.session_state.refresh_products = False

# Streamlit UI
st.title("Pharmacy Management")

# Sidebar for collection selection and search
search_collections_query = st.sidebar.text_input("Search Collections")

# Filter collections based on search query
filtered_collections = [c for c in st.session_state.collections if search_collections_query.lower() in c.lower()]

# Ensure there is always a selected collection
if not filtered_collections:
    filtered_collections = ["all"]
selected_collection = st.sidebar.radio("Select Collection", filtered_collections, index=0)

# Edit mode
edit_mode = st.sidebar.checkbox("Edit")

if edit_mode:
    st.sidebar.subheader("Delete a Collection")
    collection_to_delete = st.sidebar.selectbox("Select Collection to Delete", st.session_state.collections[1:])
    delete_button = st.sidebar.button("Delete Collection")
    
    if delete_button:
        if collection_to_delete:
            delete_collection(collection_to_delete)
            st.session_state.collections.remove(collection_to_delete)
            st.rerun()
        else:
            st.sidebar.error("Please select a collection to delete")

    st.sidebar.subheader("Add a New Collection")
    new_collection_name = st.sidebar.text_input("New Collection Name")
    add_collection_button = st.sidebar.button("Add Collection")
    
    if add_collection_button:
        if new_collection_name:
            if new_collection_name not in db.list_collection_names():
                create_collection(new_collection_name)
                st.session_state.collections.append(new_collection_name)
                st.rerun()
            else:
                st.sidebar.error(f"Collection {new_collection_name} already exists")
        else:
            st.sidebar.error("Please enter a name for the new collection")

# Display products
st.subheader("Products in Stock")

# Fetch and display products from the selected collection or all collections
products = get_products(selected_collection)

# Convert products to DataFrame
if products:
    product_df = pd.DataFrame(products)
    product_df["expiry_date"] = product_df["expiry_date"].apply(lambda x: x.strftime('%Y-%m-%d'))
    product_df["added_date"] = product_df["added_date"].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))

    # Search bar for products
    search_query = st.text_input("Search Products")
    if search_query:
        mask = product_df.apply(lambda row: search_query.lower() in ' '.join(map(str, row.values)).lower(), axis=1)
        product_df = product_df[mask]

    st.dataframe(product_df[['name', 'brand', 'dosage', 'form', 'price', 'stock', 'expiry_date', 'added_date']])
else:
    st.info("No products found")

# Add a new product
if selected_collection == "all":
    st.subheader("Add a New Product to a Collection")
else:
    st.subheader(f"Add a New Product to {selected_collection.capitalize()}")

name = st.text_input("Product Name")
brand = st.text_input("Brand")
dosage = st.text_input("Dosage")
form_ = st.text_input("Form")
price = st.number_input("Price", min_value=0.0, step=0.1)
stock = st.number_input("Stock", min_value=0, step=1)
expiry_date = st.date_input("Expiry Date")

add_button = st.button("Add Product")

if add_button:
    if name and brand and dosage and form_ and price and stock and expiry_date:
        product_data = {
            "name": name,
            "brand": brand,
            "dosage": dosage,
            "form": form_,
            "price": price,
            "stock": stock,
            "expiry_date": datetime.combine(expiry_date, datetime.min.time()),
            "added_date": datetime.now()
        }
        if selected_collection != "all":
            if selected_collection in st.session_state.collections:
                add_product(product_data, selected_collection)
                st.session_state.refresh_products = True
                st.success(f"Product {name} added successfully to {selected_collection.capitalize()}")
                st.rerun()
            else:
                st.error(f"Collection {selected_collection} does not exist.")
        else:
            st.error("Please select a specific collection to add the product")
    else:
        st.error("Please fill in all fields")

# Remove a product
st.subheader("Remove a Product")
remove_name = st.text_input("Name of the product to remove")
remove_button = st.button("Remove Product")

if remove_button:
    if remove_name:
        for collection in st.session_state.collections[1:]:  # Skip 'all' in collections
            remove_product({"name": remove_name}, collection)
        st.session_state.refresh_products = True
        st.success(f"Product {remove_name} removed successfully")
        st.rerun()
    else:
        st.error("Please enter the name of the product to remove")
