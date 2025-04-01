import mysql.connector
import datetime
from up import prg  # Import the function from your existing code

# ✅ Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="ParkingSystem"
)
cursor = conn.cursor(buffered=True)  # ✅ Use buffered cursor to handle results properly

def process_exit():
    """ Reads plate number, checks existence, updates exit time, and generates bill """
    plate_number = prg()  # Read the number plate from camera

    if not plate_number:
        print("Error: No plate detected!")
        return

    # ✅ Check if vehicle exists and hasn't exited yet
    cursor.execute("SELECT entry_time, parking_slot FROM parking_records WHERE plate_number = %s AND exit_time IS NULL", (plate_number,))
    result = cursor.fetchone()

    if not result:
        print(f"Error: No active parking record found for {plate_number}.")
        return

    entry_time, parking_slot = result
    exit_time = datetime.datetime.now()

    # ✅ Ensure all previous results are read before executing another query
    cursor.fetchall()  # ⚠️ This prevents unread result errors

    # ✅ Calculate duration in hours
    duration_hours = (exit_time - entry_time).total_seconds() / 3600
    duration_hours = max(duration_hours, 1)  # Minimum charge for 1 hour

    # ✅ Calculate Fee (₹10 per hour)
    fee = round(duration_hours * 10, 2)

    # ✅ Update exit time and fee in database
    cursor.execute(
        "UPDATE parking_records SET exit_time = %s, fee = %s WHERE plate_number = %s AND exit_time IS NULL",
        (exit_time, fee, plate_number)
    )
    conn.commit()

    # ✅ Print Bill
    print("\n========= PARKING BILL =========")
    print(f"Plate Number: {plate_number}")
    print(f"Parking Slot: {parking_slot}")
    print(f"Entry Time  : {entry_time}")
    print(f"Exit Time   : {exit_time}")
    print(f"Duration    : {round(duration_hours, 2)} hours")
    print(f"Total Fee   : ₹{fee}")
    print("================================\n")

# ✅ Run Exit Process
process_exit()

# ✅ Close the database connection
cursor.close()
conn.close()

