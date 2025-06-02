
import mysql.connector
import getpass

class ClinicSystem:
    def __init__(self):
        try:
            self.db = mysql.connector.connect(
                host="localhost",
                user="root",
                database="healthcaredb", 
                password="Shreeraj@123",
                auth_plugin="mysql_native_password"
            )
            self.cursor = self.db.cursor()
            self.current_user_name = "" 
            self.current_admin_name = "" 
            self.clinic_name = "HealthPlus Clinic" 
            self.create_tables()
            self.insert_initial_doctors() 
        except mysql.connector.Error as err:
            print(f"Error connecting to the database: {err}")
            print("Please ensure MySQL is running, the 'clinic_db' database exists, and your credentials are correct.")
            exit()

    def create_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            password VARCHAR(100),
            email VARCHAR(100) UNIQUE
        )""")
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS doctors (
            id INT AUTO_INCREMENT PRIMARY KEY,
            department VARCHAR(100), 
            doctor_name VARCHAR(255) 
        )""")
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS booked_appointments (
            appointment_id INT AUTO_INCREMENT PRIMARY KEY, 
            doctor_name VARCHAR(255),
            department VARCHAR(100),
            booked_by_patient_name VARCHAR(100) 
        )""")
        self.db.commit()

    def insert_initial_doctors(self):
        initial_doctors_data = [
             ("Cardiology", "Dr. Adhiraj Bhosale"),
             ("Dermatology", "Dr. Omkar patne"),
            ("General Medicine", "Dr. Shubham Sawant"),
             ("Orthopedics", "Dr. Uma Bhosle"),
            ("Pediatrics", "Dr. Mansi Ranjane")
            
           
        ]
        for dept, doc_name in initial_doctors_data:
        
            self.cursor.execute("SELECT 1 FROM doctors WHERE department=%s AND doctor_name=%s", (dept, doc_name))
            if not self.cursor.fetchone():
                self.cursor.execute("INSERT INTO doctors (department, doctor_name) VALUES (%s, %s)", (dept, doc_name))
        self.db.commit()


    def patient_registration(self):
        name = input("Enter your name to register: ").strip()
        if not name or name.isdigit():
            print("  x-x-x-x  Please enter a valid name  x-x-x-x  ")
            return

        email = input("Enter your E-mail: ").strip().lower()
        if "@gmail.com" not in email:
            print("  x-x-x-x  Please enter a valid E-mail (e.g., your@gmail.com)  x-x-x-x  ")
            return

        self.cursor.execute("SELECT 1 FROM patients WHERE email = %s", (email,))
        if self.cursor.fetchone():
            print("  x-x-x-x  This E-mail is already registered  x-x-x-x  ")
            return

        password = getpass.getpass("Create password: ").strip()
        if not password or len(password) < 4: 
            print("  x-x-x-x  Password must be at least 4 characters long and not empty  x-x-x-x  ")
            return

        try:
            self.cursor.execute("INSERT INTO patients (name, password, email) VALUES (%s, %s, %s)", (name, password, email))
            self.db.commit()
            print("Your registration completed successfully. You can now log in.")
        except mysql.connector.Error as err:
            print(f"Error during registration: {err}")
            self.db.rollback()


    def admin_login(self): 
        self.current_admin_name = input("Enter your name: ").strip()
        if self.current_admin_name.lower() == "admin":
            password = getpass.getpass("Enter password: ").strip()
            if password == "1220":
                print("----->| Welcome Administrator |<-----")
                while True:
                    print("....................")
                    print("\n1.Display Available Doctors \n2.Add Doctor \n3.Remove Doctor  \n4.View Booked Appointments \n5.View All Patients \n6.Logout ")
                    print("....................")
                    choice2 = input("Enter your choice: ").strip()
                    if choice2 == "1":
                        self.display_available_doctors()
                    elif choice2 == "2":
                        self.add_doctor()
                    elif choice2 == "3":
                        self.remove_doctor()
                    elif choice2 == "4":
                        self.view_all_booked_appointments()
                    elif choice2 == "5":
                        self.view_all_patients()
                    elif choice2 == "6":
                        self.current_admin_name = "" 
                        print("Logging out from admin account.")
                        break
                    else:
                        print("  x-x-x-x  Please enter a valid choice  x-x-x-x  ")
            else:
                print("  x-x-x-x  Incorrect Password  x-x-x-x  ")
        else:
            print("  x-x-x-x  Invalid Administrator name  x-x-x-x  ")

    def patient_login(self):
        email = input("Enter your E-mail: ").strip().lower()
        if "@gmail.com" not in email:
            print("  x-x-x-x  Please enter a valid E-mail  x-x-x-x  ")
            return

        self.cursor.execute("SELECT name, password FROM patients WHERE email=%s", (email,))
        result = self.cursor.fetchone()
        if result:
            self.current_user_name = result[0] 
            password = getpass.getpass("Enter password: ").strip()
            if password == result[1]:
                print(f"----->| Welcome {self.current_user_name} |<-----")
                while True:
                    print("....................")
                    print("1:Display Available Doctors \n2:Book Appointment \n3.Cancel Appointment \n4.View My Appointments \n5:Logout ") # Added "View My Appointments"
                    print("....................")
                    choice1 = input("Enter your choice: ").strip()
                    if choice1 == "1":
                        self.display_available_doctors()
                    elif choice1 == "2":
                        self.book_appointment()
                    elif choice1 == "3":
                        self.cancel_appointment()
                    elif choice1 == "4": 
                        self.view_my_appointments()
                    elif choice1 == "5":
                        print("Thank you for visiting HealthPlus Clinic")
                        self.current_user_name = "" 
                        break
                    else:
                        print("  x-x-x-x  Please enter a valid choice  x-x-x-x   ")
            else:
                print("  x-x-x-x  Incorrect Password   x-x-x-x  ")
        else:
            print("  x-x-x-x  E-mail not registered  x-x-x-x  ")

    def display_available_doctors(self): 
        self.cursor.execute("SELECT DISTINCT department FROM doctors ORDER BY department")
        departments = [d[0] for d in self.cursor.fetchall()]
        if not departments:
            print("No departments or doctors available at the moment.")
            return

        print("\n--- Available Departments ---")
        for i, department in enumerate(departments, start=1):
            print(f"{i}. {department}")

        try:
            choice = input("Select a department by number to view doctors: ").strip()
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(departments):
                selected_department = departments[choice_idx]
                self.cursor.execute("SELECT doctor_name FROM doctors WHERE department=%s ORDER BY doctor_name", (selected_department,))
                doctors = self.cursor.fetchall()
                print(f"\n--- Doctors in {selected_department} ---")
                if not doctors:
                    print("No doctors available in this department.")
                else:
                    for doctor in doctors:
                        print(f"--> {doctor[0]}")
            else:
                print("  x-x-x-x  Invalid department choice  x-x-x-x  ")
        except ValueError:
            print("  x-x-x-x  Please enter a valid number  x-x-x-x  ")

    def book_appointment(self): 
        if not self.current_user_name:
            print("Please log in as a patient to book an appointment.")
            return

        self.display_available_doctors() 
        department = input("Enter the department for the appointment: ").strip()
        doctor_name = input("Enter the full doctor's name you wish to book (e.g., 'Dr. Emily Smith'): ").strip()

    
        self.cursor.execute(
            "SELECT id FROM doctors WHERE department=%s AND doctor_name=%s",
            (department, doctor_name)
        )
        doctor_record = self.cursor.fetchone()

        if not doctor_record:
            print(f"  x-x-x-x  Doctor '{doctor_name}' not found in '{department}' or not available.  x-x-x-x  ")
            return

        self.cursor.execute("SELECT 1 FROM booked_appointments WHERE doctor_name=%s", (doctor_name,))
        if self.cursor.fetchone():
            print(f"  x-x-x-x  Dr. {doctor_name} is already booked by someone else.  x-x-x-x  ")
            return

        self.cursor.execute("SELECT 1 FROM booked_appointments WHERE booked_by_patient_name=%s", (self.current_user_name,))
        if self.cursor.fetchone():
            print(f"  x-x-x-x  You ({self.current_user_name}) already have an appointment booked. Please cancel it first if you wish to book another.  x-x-x-x  ")
            return

        try:
        
            self.cursor.execute("DELETE FROM doctors WHERE id=%s", (doctor_record[0],))
            
            self.cursor.execute(
                "INSERT INTO booked_appointments (doctor_name, department, booked_by_patient_name) VALUES (%s, %s, %s)",
                (doctor_name, department, self.current_user_name)
            )
            self.db.commit()
            print(f"Appointment with {doctor_name} in {department} has been successfully booked for {self.current_user_name}.")
        except mysql.connector.Error as err:
            print(f"Error booking appointment: {err}")
            self.db.rollback()


    def cancel_appointment(self): 
        if not self.current_user_name:
            print("Please log in as a patient to cancel an appointment.")
            return

        self.view_my_appointments() 
        doctor_name = input("Enter the full doctor's name for the appointment you wish to cancel: ").strip()

        self.cursor.execute(
            "SELECT department, appointment_id FROM booked_appointments WHERE doctor_name=%s AND booked_by_patient_name=%s",
            (doctor_name, self.current_user_name)
        )
        booked_appointment_details = self.cursor.fetchone()

        if not booked_appointment_details:
            print(f"  x-x-x-x  No appointment with {doctor_name} found booked by you ({self.current_user_name}).  x-x-x-x  ")
            return

        department, appointment_id = booked_appointment_details
        
        try:

            self.cursor.execute("DELETE FROM booked_appointments WHERE appointment_id=%s", (appointment_id,))
            
            self.cursor.execute("INSERT INTO doctors (department, doctor_name) VALUES (%s, %s)", (department, doctor_name))
            self.db.commit()
            print(f"Your appointment with {doctor_name} in {department} has been successfully cancelled.")
        except mysql.connector.Error as err:
            print(f"Error cancelling appointment: {err}")
            self.db.rollback()

    def view_my_appointments(self): 
        if not self.current_user_name:
            print("Please log in to view your appointments.")
            return
        
        self.cursor.execute(
            "SELECT department, doctor_name FROM booked_appointments WHERE booked_by_patient_name=%s",
            (self.current_user_name,)
        )
        my_bookings = self.cursor.fetchall()

        if not my_bookings:
            print(f"You ({self.current_user_name}) currently have no appointments booked.")
        else:
            print(f"\n--- Your Booked Appointments ({self.current_user_name}) ---")
            print(f"{'Department':<20} | {'Doctor':<25}")
            print("-" * 47)
            for dept, doc_name in my_bookings:
                print(f"{dept:<20} | {doc_name:<25}")


    def add_doctor(self):
        department = input("Enter the doctor's department (e.g., Cardiology): ").strip()
        doctor_name = input("Enter the doctor's full name (e.g., Dr. Jane Doe): ").strip()

        if not department or not doctor_name:
            print("  x-x-x-x  Department and doctor name cannot be empty.  x-x-x-x  ")
            return

        self.cursor.execute("SELECT 1 FROM doctors WHERE department=%s AND doctor_name=%s", (department, doctor_name))
        if self.cursor.fetchone():
            print("  x-x-x-x  This doctor already exists in this department.  x-x-x-x  ")
            return
        
        try:
            self.cursor.execute("INSERT INTO doctors (department, doctor_name) VALUES (%s, %s)", (department, doctor_name))
            self.db.commit()
            print(f"Dr. {doctor_name} has been added to the {department} department.")
        except mysql.connector.Error as err:
            print(f"Error adding doctor: {err}")
            self.db.rollback()

    def remove_doctor(self): 
        department = input("Enter the department of the doctor to remove: ").strip()
        doctor_name = input("Enter the full name of the doctor to remove: ").strip()

        self.cursor.execute("SELECT id FROM doctors WHERE department=%s AND doctor_name=%s", (department, doctor_name))
        doctor_record = self.cursor.fetchone()
        
        if not doctor_record:
            print(f"  x-x-x-x  Dr. {doctor_name} not found in the {department} department.  x-x-x-x  ")
            return

        
        self.cursor.execute("SELECT 1 FROM booked_appointments WHERE doctor_name=%s", (doctor_name,))
        if self.cursor.fetchone():
            print(f"  x-x-x-x  Cannot remove Dr. {doctor_name} as they have a booked appointment. Please cancel it first.  x-x-x-x  ")
            return
        
        try:
            self.cursor.execute("DELETE FROM doctors WHERE id=%s", (doctor_record[0],))
            self.db.commit()
            print(f"Dr. {doctor_name} has been removed from the {department} department.")
        except mysql.connector.Error as err:
            print(f"Error removing doctor: {err}")
            self.db.rollback()

    def view_all_booked_appointments(self): 
        self.cursor.execute("SELECT department, doctor_name, booked_by_patient_name FROM booked_appointments ORDER BY department, doctor_name")
        records = self.cursor.fetchall()
        if not records:
            print("No appointments have been booked yet.")
        else:
            print("\n--- All Booked Appointments ---")
            print(f"{'Department':<20} | {'Doctor':<25} | {'Booked By Patient':<25}")
            print("-" * 75)
            for dept, doc_name, patient_name in records:
                print(f"{dept:<20} | {doc_name:<25} | {patient_name:<25}")

    def view_all_patients(self):
        self.cursor.execute("SELECT name, email FROM patients ORDER BY name")
        users = self.cursor.fetchall()
        if not users:
            print("No patients registered yet.")
        else:
            print("\n--- Registered Patients ---")
            print(f"{'Name':<20} | {'Email':<30}")
            print("-" * 52)
            for name, email in users:
                print(f"{name:<20} | {email:<30}")

    def home(self): 
        print(f"\n----->| Welcome to {self.clinic_name} |<-----")
        while True:
            print("....................")
            print("1: Administrator Login \n2: Patient Login \n3: Patient Registration \n4: Exit")
            print("....................")
            choice = input("Enter your choice: ").strip()
            if choice == "1":
                self.admin_login()
            elif choice == "2":
                self.patient_login()
            elif choice == "3":
                self.patient_registration()
            elif choice == "4":
                print("Thank you for using HealthPlus Clinic. Goodbye!")
                break
            else:
                print("  x-x-x-x  Please enter a valid choice  x-x-x-x   ")

        
        if self.db.is_connected():
            self.cursor.close()
            self.db.close()
            print("Database connection closed.")

if __name__ == "__main__":
    clinic = ClinicSystem()
    clinic.home()
