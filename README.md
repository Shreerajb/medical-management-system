# HealthPlus Clinic Management System

The **HealthPlus Clinic Management System** is a command-line Python application designed to manage a basic clinic environment using **Core Python** and **MySQL**. It allows for patient registration, login, appointment booking/cancellation, and admin functionalities such as doctor management and appointment tracking.

---

## 🚀 Features

### Patient Side
- ✅ Patient Registration
- ✅ Secure Patient Login
- ✅ View Available Doctors by Department
- ✅ Book Appointment with a Doctor
- ✅ Cancel Appointment
- ✅ View Your Booked Appointments

### Admin Side
- 🔐 Admin Login (Default credentials: `admin` / `1220`)
- 👩‍⚕️ Add or Remove Doctors
- 📋 View All Doctors by Department
- 🧾 View All Registered Patients
- 🗓️ View All Booked Appointments

---

## 🛠 Technologies Used

- **Python 3**
- **MySQL** (via `mysql-connector-python`)
- **getpass** for secure password input

---

## 🏗️ Database Setup

1. Create a database named `healthcaredb` in MySQL:
    ```sql
    CREATE DATABASE healthcaredb;
    ```

2. No need to manually create tables – they will be created automatically when you run the script.

---

## ⚙️ Installation and Running

### Prerequisites:
- Python installed (`3.8` or later recommended)
- MySQL server running
- Python package: `mysql-connector-python`

### Steps:
1. Install the required package (if not already):
    ```bash
    pip install mysql-connector-python
    ```

2. Update the database credentials in the script if needed:
    ```python
    user="root",
    password="Shreeraj@123",
    host="localhost",
    database="healthcaredb"
    ```

3. Run the script:
    ```bash
    python clinic.py
    ```

---

## 📌 Default Data

- The system automatically inserts 5 doctors across different departments on first run.
- Admin login:
    - **Username:** `admin`
    - **Password:** `1220`

---

## 📎 File Structure

