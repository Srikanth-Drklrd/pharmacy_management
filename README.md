# **Pharmacy Database Management System**

## **Project Description**
The **Pharmacy Database Management System** is a comprehensive application for managing pharmacy inventory. Built using **Streamlit** and **Tkinter**, it offers two different user interfaces (web-based and desktop) for greater flexibility. This system enables efficient tracking of stock, managing product collections, and handling critical attributes such as product details, pricing, and expiry dates.

The application uses **MongoDB** for cloud-based data storage, ensuring scalability, security, and real-time access to inventory information.

---

## **Features**
### **Web-Based Interface (Streamlit)**
- **Dynamic Product Management**:
  - Add, search, and remove products across multiple collections.
- **Collection Management**:
  - Create and delete collections for categorizing products.
- **Inventory Search**:
  - Filter and search products in real-time using advanced query options.
- **Cloud Integration**:
  - Data stored securely on MongoDB Atlas.

### **Desktop Interface (Tkinter)**
- **Tabbed Navigation**:
  - Separate tabs for managing different product categories (e.g., Tablets, Capsules, Syrups).
- **Intuitive Forms**:
  - Add new products with detailed attributes using simple input forms.
- **Inventory Display**:
  - View and search inventory items in a tree-structured table.
- **Product Removal**:
  - Delete products directly by name with validation.
- **Real-Time Database Updates**:
  - All changes reflect in the MongoDB database.

---

## **Technologies Used**
- **Frontend**:
  - Streamlit (Web-based UI)
  - Tkinter (Desktop UI)
- **Backend**:
  - Python
- **Database**:
  - MongoDB (via MongoDB Atlas)
- **Hosting**:
  - MongoDB Atlas cloud service

---

## **Setup and Installation**

### **Prerequisites**
- Python 3.8+
- MongoDB Atlas account for database access
- Required libraries: `streamlit`, `pymongo`, `pandas`, `tkinter`, `datetime`

### **Steps to Run the Web-Based Application (Streamlit)**
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/pharma-management-system.git
   cd pharma-management-system
2. **Run the Application**:
   ```bash
   streamlit run app.py

### **Steps to Run the Desktop Application (Tkinter)**
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/pharma-management-system.git
   cd pharma-management-system
2. **Run the Application**:
   ```bash
   python tkinter_app.py
