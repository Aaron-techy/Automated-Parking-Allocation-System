import mysql.connector
import datetime
from up import prg  # Import the function from your existing code

# ✅ Correct way to connect to MySQL
conn = mysql.connector.connect(
    host="localhost",  # Change if your MySQL server is on a different host
    user="root",  # Your MySQL username
    password="root",  # Your MySQL password
    database="ParkingSystem"  # Ensure the database exists
)

cursor = conn.cursor()

# ✅ Create Table if Not Exists
cursor.execute("""
    CREATE TABLE IF NOT EXISTS parking_records (
        id INT AUTO_INCREMENT PRIMARY KEY,
        plate_number VARCHAR(20) NOT NULL,
        parking_slot VARCHAR(10) NOT NULL,
        entry_time DATETIME NOT NULL,
        exit_time DATETIME NULL,
        fee DECIMAL(10,2) NULL
    )
""")

def get_available_slot():
    """ Assigns the first available slot in hexadecimal format from 1 to 50 """
    cursor.execute("SELECT parking_slot FROM parking_records WHERE exit_time IS NULL")
    occupied_slots = {slot[0] for slot in cursor.fetchall()}

    for i in range(1, 51):
        hex_slot = hex(i)[2:].upper()  # Convert to Hex (1 → '1', 10 → 'A', 50 → '32')
        if hex_slot not in occupied_slots:
            return hex_slot
    return None  # No slot available

def store_parking_record():
    """ Calls prg() to detect a plate and stores the details in the database """
    plate_number = prg()  # Call the number plate detection function

    if plate_number:
        parking_slot = get_available_slot()
        if parking_slot:
            entry_time = datetime.datetime.now()

            # ✅ Insert record into database (with `parking_slot`)
            cursor.execute(
                "INSERT INTO parking_records (plate_number, parking_slot, entry_time) VALUES (%s, %s, %s)",
                (plate_number, parking_slot, entry_time)
            )
            conn.commit()
            print(f"Stored: {plate_number} | Slot: {parking_slot} | Time: {entry_time}")
        else:
            print("No available parking slots!")
    else:
        print("No plate detected!")


# ✅ Run the function
store_parking_record()

# ✅ Close the database connection
cursor.close()
conn.close()
