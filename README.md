# Automated Parking Allocation System

## 📌 Overview

This project is an **Automated Parking Allocation System** using **OpenCV and MySQL**. It detects vehicle number plates using **Tesseract OCR**, assigns parking slots, and calculates parking fees.

## 🚀 Features

- **Number Plate Detection** using OpenCV & Tesseract
- **Automatic Parking Slot Allocation** (Hexadecimal from 1 to 50)
- **Entry & Exit Management**
- **Parking Fee Calculation** (₹10 per hour)
- **MySQL Database Integration**
- **Bill Generation upon Exit**

---

## 🛠️ Setup & Installation

### 1️⃣ Install Dependencies

Run the following command to install required Python packages:

```sh
pip install opencv-python pytesseract mysql-connector-python
```

### 2️⃣ Configure Tesseract OCR

Download and install [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki). Then, update the **Tesseract path** in `prg.py`:

```python
pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
```

### 3️⃣ MySQL Database Setup

Create a **MySQL database** and run the following SQL command to create the `parking_records` table:

```sql
CREATE DATABASE parking_db;

USE parking_db;

CREATE TABLE parking_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    plate_number VARCHAR(20) NOT NULL,
    parking_slot VARCHAR(5) NOT NULL,
    entry_time DATETIME NOT NULL,
    exit_time DATETIME DEFAULT NULL,
    fee DECIMAL(10,2) DEFAULT NULL
);
```

### 4️⃣ Update Database Credentials

Modify `entry.py` and `exit.py` with your MySQL credentials:

```python
conn = mysql.connector.connect(
    host="localhost",
    user="root",  # Change this
    password="yourpassword",  # Change this
    database="parking_db"
)
```

---

## 🚘 Usage

### 📥 Vehicle Entry (Run `entry.py`)

```sh
python entry.py
```

- **Detects plate number**
- **Assigns a parking slot**
- **Saves entry time in the database**

### 📤 Vehicle Exit (Run `exit.py`)

```sh
python exit.py
```

- **Detects plate number**
- **Checks if the vehicle exists in the database**
- **Adds exit time & calculates fee**
- **Prints the parking bill**

---

## 📜 Example Bill Output

```
========= PARKING BILL =========
Plate Number: KA01AB1234
Parking Slot: A
Entry Time  : 2025-02-11 10:00:00
Exit Time   : 2025-02-11 12:30:00
Duration    : 2.5 hours
Total Fee   : ₹25.00
================================
```

---

## 📌 Future Enhancements

- ✅ SMS/Email Notifications for Bills
- ✅ Web Dashboard for Parking Management
- ✅ Real-Time Slot Availability Tracking

📩 **Have suggestions? Feel free to contribute!** 🚀

