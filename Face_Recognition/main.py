import pickle
import numpy as np
import cv2
import os
import cvzone
import mysql.connector as my
import datetime
import face_recognition
from tabulate import tabulate

# Connect to MySQL database
mysql_conn = my.connect(
    host='localhost',
    user='root',
    password='2004',
    database='bcaibm_attendance'
)
mysql_cursor = mysql_conn.cursor()

# Get the current date
current_date_str = datetime.date.today().strftime("%d/%m/%Y")

# Execute SQL query to add column with the current date as the name and limited to 'Present' and 'Absent' values
try:
    mysql_cursor.execute("ALTER TABLE attendance ADD COLUMN `{}` ENUM('Present', 'Absent') DEFAULT 'Absent'".format(current_date_str))
    print("Column '{}' added successfully.".format(current_date_str))
except my.Error as e:
    print("MySQL Error:", e.msg)


cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread('D:\Python\Face_Recognition\Resources\ATTENDANCE SYSTEM.png')

# Importing the mode images into a list
'''
folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))'''

# Load the encoding file
print("Loading Encode File....")
file = open('EncodeFile.p', 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds
print("Encode File Loaded")

while True:
    success, img = cap.read()

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    imgBackground[162:162 + 480, 55:55 + 640] = img


    # Flags to track if known face or unknown face is detected
    known_face_detected = False
    unknown_face_detected = False

    for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        #qprint("Face Distance: ", faceDis)

        best_match_index = np.argmin(faceDis)
        best_match_distance = faceDis[best_match_index]

        if matches[best_match_index] and best_match_distance > 0.2:  # Check if accuracy is above 0.8
            known_face_detected = True
            print("Known Face Detected with high accuracy")
            print("Accuracy:", 1 - best_match_distance)  # Print the accuracy
            print(studentIds[best_match_index])
            student_id = studentIds[best_match_index]

            # Update the database with the current date
            update_query = f"UPDATE attendance SET `{current_date_str}` = 'Present' WHERE student_id = %s"
            mysql_cursor.execute(update_query, (student_id,))
            mysql_conn.commit()

            try:
                # Fetch all details of the student from the attendance table
                select_query = "SELECT * FROM attendance WHERE student_id = %s"
                mysql_cursor.execute(select_query, (student_id,))
                student_details = mysql_cursor.fetchone()
                if student_details:
                    print("Student Details:", student_details)
                else:
                    print("No details found for the student.")
            except my.Error as e:
                print("MySQL Error:", e.msg)
            except Exception as e:
                print("Error fetching student details:", e)

            # Perform further actions here like database update

            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
            imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)

        else:
            unknown_face_detected = True
            print("Unknown Face Detected. Please try again.")

            # Draw white box around the face
            '''y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(imgBackground, (55 + x1, 162 + y1), (55 + x2, 162 + y2), (255, 255, 255), 2)'''

    # Hide "Please try again" text if a known face is detected
    '''if known_face_detected:
        cv2.rectangle(imgBackground, (55, 142), (695, 142 + 30), (255, 255, 255), -1)'''

    cv2.imshow("Face Attendance", imgBackground)
    # Break out of the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()


# Get the current date
current_date_str = datetime.date.today().strftime("%d/%m/%Y")


def mark_present():
    # Implement marking someone present logic here
    # Execute SQL query to fetch the name of the student
    student_idP = int(input("Enter the student id : "))
    select_query = "SELECT name FROM attendance WHERE student_id = %s"
    mysql_cursor.execute(select_query, (student_idP,))
    student_info = mysql_cursor.fetchone()

    if student_info:
        student_name = student_info[0]
        # Execute update query to mark attendance as present
        update_query = f"UPDATE attendance SET `{current_date_str}` = 'Present' WHERE student_id = %s AND `{current_date_str}` = 'Absent'"
        try:
            mysql_cursor.execute(update_query, (student_idP,))
            mysql_conn.commit()
            print("Attendance marked as present for student ID:", student_idP, "Name:", student_name)
        except my.Error as e:
            print("MySQL Error:", e.msg)
    else:
        print("Provided student ID does not match any student ID in the database.")


def mark_absent():
    # Implement marking someone absent logic here
    # Execute SQL query to fetch the name of the student
    student_idA = int(input("Enter the student id : "))
    select_query = "SELECT name FROM attendance WHERE student_id = %s"
    mysql_cursor.execute(select_query, (student_idA,))
    student_info = mysql_cursor.fetchone()


    if student_info:
        student_name = student_info[0]
        # Execute update query to mark attendance as absent
        update_query = f"UPDATE attendance SET `{current_date_str}` = 'Absent' WHERE student_id = %s AND `{current_date_str}` = 'Present'"
        try:
            mysql_cursor.execute(update_query, (student_idA,))
            mysql_conn.commit()
            print("Attendance marked absent for student ID:", student_idA, "Name:", student_name)
        except my.Error as e:
            print("MySQL Error:", e.msg)
    else:
        print("Provided student ID does not match any student ID in the database.")


# Function to handle checking attendance
def check_attendance():
    # Implement checking attendance logic here
    try:
        # Execute SQL query to select student_id, name, and current date's attendance status
        select_query = f"SELECT student_id, name, `{current_date_str}` FROM attendance"
        mysql_cursor.execute(select_query)

        # Fetch all rows
        results = mysql_cursor.fetchall()

        # Prepare data for tabulate
        table_headers = ["Student ID", "Name", current_date_str]
        table_data = [[row[0], row[1], row[2]] for row in results]

        # Print the table
        print(tabulate(table_data, headers=table_headers, tablefmt="grid"))

    except my.Error as e:
        print("MySQL Error:", e.msg)


def check_attendanceForSpecificDate():
    # Function to handle checking attendance for a specific date
    try:
        # Ask the user for the specific date
        specific_date = input("Enter the date (DD/MM/YYYY) to check attendance: ")

        # Execute SQL query to select student_id, name, and attendance status for the specific date
        select_query = f"SELECT student_id, name, `{specific_date}` FROM attendance"
        mysql_cursor.execute(select_query)

        # Fetch all rows
        results = mysql_cursor.fetchall()

        # Prepare data for tabulate
        table_headers = ["Student ID", "Name", specific_date]
        table_data = [[row[0], row[1], row[2]] for row in results]

        # Print the table
        print(tabulate(table_data, headers=table_headers, tablefmt="grid"))

    except my.Error as e:
        print("MySQL Error:", e.msg)


# Main program loop
while True:
    print("Choose an option:")
    print("1. Mark someone present")
    print("2. Mark someone absent")
    print("3. Check attendance")
    print("4. Check attendance for Specific Date")
    print("5. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        mark_present()
    elif choice == '2':
        mark_absent()
    elif choice == '3':
        check_attendance()
    elif choice == '4':
        check_attendanceForSpecificDate()
    elif choice == '5':
        print("Exiting...")
        break
    else:
        print("Invalid choice. Please try again.")
