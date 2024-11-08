from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql

app = Flask(__name__)
app.secret_key = 'your_secret_key'


def get_db_connection():
    return pymysql.connect(host="localhost", user="root", password="root", database="hospital")
# Home Route
@app.route('/')
def home():
    return render_template('home.html')


# Index Route
@app.route('/index')
def index():
    return render_template('index.html')

# Login Route
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    connection = get_db_connection()
    cursor = connection.cursor()
    
    cursor.execute("SELECT password FROM login WHERE username = %s", (username,))
    result = cursor.fetchone()
    
    if result and result[0] == int(password):  
        return render_template('menu.html')
    else:
        flash("Incorrect login credentials", "danger")
        return redirect(url_for('index'))






@app.route('/doctors', methods=['GET', 'POST'])
def add_doctors():
    connection = get_db_connection()
    cursor = connection.cursor()

    if request.method == 'POST':
        # Adjusted to match form field names in the request data
        doctor_id = request.form.get('docid')
        doctor_name = request.form.get('docname')
        department = request.form.get('department')  # Make sure form input name is 'department'
        phone = request.form.get('phone')
        password = request.form.get('password')

        # Check if all required fields are provided
        if doctor_id and doctor_name and department and phone and password:
            try:
                # Insert doctor data into the doctor table
                cursor.execute(
                    "INSERT INTO doctor (DOCID, DOCNAME, DEPARTMENT, PHNO) VALUES (%s, %s, %s, %s)", 
                    (doctor_id, doctor_name, department, phone)
                )

                # Insert login data into the login table for the doctor
                cursor.execute(
                    "INSERT INTO login (username, password, designation) VALUES (%s, %s, %s)", 
                    (doctor_id, password, "doctor")
                )

                # Commit the transaction
                connection.commit()
                flash("Doctor added successfully!", "success")
                return redirect(url_for('view_doctors'))  # Redirect to avoid re-submission

            except Exception as e:
                connection.rollback()
                flash(f"An error occurred while adding the doctor: {e}", "danger")
        else:
            flash("Please fill in all the fields.", "warning")

    # Fetch all doctors to display in the table
    cursor.execute("SELECT * FROM doctor")
    doctors = cursor.fetchall()
    connection.close()

    return render_template('add_doctors.html', doctors=doctors)









@app.route('/add_staff', methods=['GET', 'POST'])
def add_staff():
    connection = get_db_connection()
    cursor = connection.cursor()

    if request.method == 'POST':
        staff_id = request.form['staff_id']
        staff_name = request.form['staff_name']
        staff_age = request.form['staff_age']
        staff_work = request.form['staff_work']  
        phone = request.form['phone']
        password = request.form['password']  

        cursor.execute("INSERT INTO staff (STAFF_ID, STAFF_NAME, STAFF_AGE, STAFF_WORK, PHNO) VALUES (%s, %s, %s, %s, %s)", 
                       (staff_id, staff_name, staff_age, staff_work, phone))
        
        cursor.execute("INSERT INTO login (username, password, designation) VALUES (%s, %s, %s)", 
                       (staff_id, password, staff_work))  

        connection.commit()

    cursor.execute("SELECT * FROM staff")
    staff_members = cursor.fetchall()
    connection.close()

    return render_template('add_staff.html', staff=staff_members)

    connection = get_db_connection()
    cursor = connection.cursor()

    if request.method == 'POST':
        staff_id = request.form['staff_id']
        staff_name = request.form['staff_name']
        staff_age = request.form['staff_age']
        staff_work = request.form['staff_work']
        phone = request.form['phone']

        # Insert into staff table
        cursor.execute("INSERT INTO staff (STAFF_ID, STAFF_NAME, STAFF_AGE, STAFF_WORK, PHNO) VALUES (%s, %s, %s, %s, %s)", 
                       (staff_id, staff_name, staff_age, staff_work, phone))
        
        # Insert into login table only if staff work is 'Receptionist'
        if staff_work.lower() == 'receptionist':
            cursor.execute("INSERT INTO login (username, password) VALUES (%s, %s)", 
                           (staff_id, "default_password"))  # Again, use a secure password strategy

        connection.commit()
        flash("Staff member added successfully!", "success")

    cursor.execute("SELECT * FROM staff")
    staff_members = cursor.fetchall()
    connection.close()

    return render_template('add_staff.html', staff=staff_members)


@app.route('/patients', methods=['GET', 'POST'])
def add_patients():
    connection = get_db_connection()
    cursor = connection.cursor()

    if request.method == 'POST':
        patient_id = request.form['patient_id']
        patient_name = request.form['patient_name']
        patient_age = request.form['patient_age']
        diseases = request.form['diseases']
        phone = request.form['phone']
        docid=request.form['docid']
        docname=request.form['docname']
        cursor.execute("INSERT INTO patient (PATIENT_ID, PATIENT_NAME, PATIENT_AGE, DISEASES, PHNO,docid,docname) VALUES (%s, %s, %s, %s, %s,%s,%s)", 
                       (patient_id, patient_name, patient_age, diseases, phone,docid,docname))
        connection.commit()

    cursor.execute("SELECT * FROM patient")
    patients = cursor.fetchall()
    connection.close()

    return render_template('add_patients.html', patients=patients)

# Staff Management

#==========================================================================================
# View Doctor Details
@app.route('/view_doctors', methods=['GET', 'POST'])
def view_doctors():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM doctor")
    doctors = cursor.fetchall()
    connection.close()
    return render_template('view_doctors.html', doctors=doctors)

# View Patient Details
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
    cursor.execute("SELECT * FROM staff")
    staff_members = cursor.fetchall()
    connection.close()
    return render_template('view_staff.html', staff=staff_members)



#==============================================================================================







@app.route('/delete_patient/<int:patient_id>', methods=['POST'])
def delete_patient(patient_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    try:
        cursor.execute("DELETE FROM patient WHERE PATIENT_ID = %s", (patient_id,))
        connection.commit()
        
        if cursor.rowcount == 0:
            flash("Patient not found or already deleted.", "warning")
        else:
            flash("Patient deleted successfully!", "success")
    
    except Exception as e:
        flash(f"An error occurred: {e}", "danger")
    
    finally:
        connection.close()

    return redirect(url_for('view_patients'))


@app.route('/delete_doctor/<int:doctor_id>', methods=['POST'])
def delete_doctor(doctor_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("DELETE FROM doctor WHERE DOCTOR_ID = %s", (doctor_id,))
        connection.commit()

        if cursor.rowcount == 0:
            flash("Doctor not found or already deleted.", "warning")
        else:
            flash("Doctor deleted successfully!", "success")

    except Exception as e:
        flash(f"An error occurred: {e}", "danger")

    finally:
        connection.close()

    return redirect(url_for('view_doctors'))


@app.route('/delete_staff/<int:staff_id>', methods=['POST'])

def delete_staff(staff_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("DELETE FROM staff WHERE STAFF_ID = %s", (staff_id,))
        connection.commit()

        if cursor.rowcount == 0:
            flash("Staff member not found or already deleted.", "warning")
        else:
            flash("Staff member deleted successfully!", "success")

    except Exception as e:
        flash(f"An error occurred: {e}", "danger")

    finally:
        connection.close()

    return redirect(url_for('view_staff'))















if __name__ == "__main__":
    app.run(debug=True)
