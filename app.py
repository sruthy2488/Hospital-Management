from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql


app = Flask(__name__)
app.secret_key = 'your_secret_key'


def get_db_connection():
    return pymysql.connect(host="localhost", user="root", password="root", database="hospital")

#===========================================================================================================

@app.route('/')
def home():
    return render_template('home.html')

#=============================================================================================================
@app.route('/index')
def index():
    return render_template('index.html')
              

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    connection = get_db_connection()
    cursor = connection.cursor()
    
    cursor.execute("SELECT password, designation FROM login WHERE username = %s", (username,))
    result = cursor.fetchone()
    
    if result and str(result[0]) == password:  
        designation = result[1].lower()  
        
        if designation == "doctor":
            return redirect(url_for('doctor_dashboard'))
        elif designation == "receptionist":
             return render_template('menu.html')
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))


#==============================================================================================================

@app.route('/viewonly_doctors')
def viewonly_doctors():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM doctor")
    doctors = cursor.fetchall()
    connection.close()
    return render_template('viewonly_doctors.html', doctors=doctors)



@app.route('/viewonly_staff')
def viewonly_staff():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM staff")
    staff = cursor.fetchall()
    connection.close()
    return render_template('viewonly_staff.html', staff=staff) 



@app.route('/viewonly_patient')
def viewonly_patient():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM patient")
    patients = cursor.fetchall()  
    connection.close()
    return render_template('viewonly_patient.html', patients=patients)  



@app.route('/doctor_dashboard')
def doctor_dashboard():
    return render_template('doctor_dashboard.html')



@app.route('/receptionist_dashboard')
def receptionist_dashboard():
    return render_template('receptionist_dashboard.html')





#==================================================================================================================

@app.route('/doctors', methods=['GET', 'POST'])
def add_doctors():
    connection = get_db_connection()
    cursor = connection.cursor()

    if request.method == 'POST':
        doctor_name = request.form.get('docname')
        department = request.form.get('department')
        phone = request.form.get('phone')
        password = request.form.get('password')
        print(f"Doctor Name: {doctor_name}, Department: {department}, Phone: {phone}, Password: {password}")

        if doctor_name and department and phone and password:
        
                cursor.execute("SELECT DOCID FROM doctor ORDER BY DOCID DESC LIMIT 1")
                result = cursor.fetchone()

                if result:
                    next_id = int(result[0][1:]) + 1  
                else:
                    next_id = 1001  

                docid = f"D{next_id}"
                cursor.execute(
                    "INSERT INTO doctor (DOCID, DOCNAME, DEPARTMENT, PHNO) VALUES (%s, %s, %s, %s)", 
                    (docid, doctor_name, department, phone)
                )

                cursor.execute(
                    "INSERT INTO login (username, password, designation) VALUES (%s, %s, %s)", 
                    (docid, password, "doctor")
                )

                connection.commit()
                return redirect(url_for('viewonly_doctors')) 

           
        
    cursor.execute("SELECT * FROM doctor")
    doctors = cursor.fetchall()
    connection.close()

    return render_template('add_doctors.html', doctors=doctors)





@app.route('/add_staff', methods=['GET', 'POST'])
def add_staff():
    connection = get_db_connection()
    cursor = connection.cursor()

    if request.method == 'POST':
        staff_name = request.form['staff_name']
        staff_age = request.form['staff_age']
        staff_work = request.form['staff_work']
        phone = request.form['phone']

        cursor.execute("SELECT STAFF_ID FROM staff ORDER BY STAFF_ID DESC LIMIT 1")
        last_staff_id = cursor.fetchone()

        if last_staff_id:
            last_number = int(last_staff_id[0][1:])  
            next_staff_id = last_number + 1  
        else:
            next_staff_id = 1   

        formatted_staff_id = f"S{next_staff_id:04d}"

        cursor.execute("""
            INSERT INTO staff (STAFF_ID, STAFF_NAME, STAFF_AGE, STAFF_WORK, PHNO) 
            VALUES (%s, %s, %s, %s, %s)
        """, (formatted_staff_id, staff_name, staff_age, staff_work, phone))

        connection.commit()
        return redirect(url_for('viewonly_staff')) 

    cursor.execute("SELECT * FROM staff")
    staff_members = cursor.fetchall()

    connection.close()

    return render_template('add_staff.html', staff=staff_members)






@app.route('/patients', methods=['GET', 'POST'])
def add_patients():
    connection = get_db_connection()
    cursor = connection.cursor()

    # Fetch all doctors to display in the dropdown list
    cursor.execute("SELECT DOCID, DOCNAME FROM doctor")
    doctors = cursor.fetchall()

    if request.method == 'POST':
        patient_name = request.form['patient_name']
        patient_age = request.form['patient_age']
        diseases = request.form['diseases']
        phone = request.form['phone']
        docname = request.form['docname']

        # Fetch the doctor’s name using the docid
        cursor.execute("SELECT DOCID FROM doctor WHERE DOCNAME = %s", (docname,))
        doctor = cursor.fetchone()

        if doctor:
            docid = doctor[0]  # Extract the doctor's name from the result

            # Fetch the last patient ID to generate the next one
            cursor.execute("SELECT MAX(PATIENT_ID) FROM patient")
            last_patient_id = cursor.fetchone()[0]

            # Generate the next patient ID (increment last number after "P")
            if last_patient_id:
                # Extract the numeric part of the last patient ID
                last_patient_number = int(last_patient_id[1:])  # Remove "P" and convert to int
                new_patient_number = last_patient_number + 1
            else:
                new_patient_number = 1  # First patient, start with P001

            # Format the new patient ID
            new_patient_id = f"P{new_patient_number:03d}"

            # Insert the patient into the patient table
            cursor.execute("""
                INSERT INTO patient (PATIENT_ID, PATIENT_NAME, PATIENT_AGE, DISEASES, PHNO, DOCID, DOCNAME) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (new_patient_id, patient_name, patient_age, diseases, phone, docid, docname))

            connection.commit()
            return redirect(url_for('view_patients'))
       
    
    # Fetch all patients to display in the table
    cursor.execute("SELECT * FROM patient")
    patients = cursor.fetchall()
    connection.close()

    return render_template('add_patients.html', patients=patients, doctors=doctors)




#==========================================================================================
@app.route('/view_doctors', methods=['GET', 'POST'])
def view_doctors():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM doctor")
    doctors = cursor.fetchall()
    connection.close()
    return render_template('view_doctors.html', doctors=doctors)




@app.route('/view_patients', methods=['GET', 'POST'])
def view_patients():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM patient")
    patients = cursor.fetchall()
    connection.close()
    return render_template('view_patients.html', patients=patients)




@app.route('/view_staff', methods=['GET', 'POST'])
def view_staff():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM staff where staff_work !='Receptionist'")
    staff_members = cursor.fetchall()
    connection.close()
    return render_template('view_staff.html', staff=staff_members)



#==============================================================================================

@app.route('/delete_patient/<string:patient_id>', methods=['POST'])
def delete_patient(patient_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    
    cursor.execute("DELETE FROM patients WHERE PATIENT_ID = %s", (patient_id,))
    connection.commit()
    connection.close()

    return redirect(url_for('view_patients'))




@app.route('/delete_doctor/<doctor_id>', methods=['POST'])
def delete_doctor(doctor_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    
    cursor.execute("DELETE FROM login WHERE username = %s", (doctor_id,))

    cursor.execute("DELETE FROM doctor WHERE DOCID = %s", (doctor_id,))

    connection.commit()
    connection.close()

    return redirect(url_for('view_doctors'))




@app.route('/delete_staff/<string:staff_id>', methods=['POST'])
def delete_staff(staff_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    
    cursor.execute("DELETE FROM staff WHERE STAFF_ID = %s", (staff_id,))
    connection.commit()
    return redirect(url_for('view_staff'))




if __name__ == "__main__":
    app.run(debug=True)
