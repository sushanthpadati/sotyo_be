from flask import Flask, request, jsonify, session
from flask_cors import CORS
import mysql.connector
import os
app = Flask(__name__)
CORS(app, supports_credentials=True)  # Enable credentials for cookies/session

app.secret_key = os.urandom(24)  # Set a secret key for session management

mydb = mysql.connector.connect(
    host="localhost",
    username="satyam",
    password = "satyam_321",
    database="sotyo_db"
)
print(mydb)

@app.route("/")
def main():
    cursor = mydb.cursor()
    cursor.execute("SELECT DATABASE()")
    database_name = cursor.fetchone()[0]
    cursor.close()

    return f"Flask is installed. Database connection established. Connected to database successfully done"

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT * FROM login WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()
    cursor.close()

    if user:
        session['user_id'] = user['id']
        session['name'] = user['name']
        session['profession'] = user['profession']

        return jsonify({'success': True, 'message': 'Login successful', 'user': {'name': user['name'], 'profession': user['profession']}})
    else:
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
@app.route('/add', methods=['POST'])
def submit():
    if request.method == 'POST':
        try:
            data = request.get_json()
            if 'firstname' in data:
                firstname = data['firstname']
                lastname = data['lastname']
                sex = data.get('sex', '')
                marital_status = data.get('marital', '')
                dob = data.get('dob', None)
                organ = data.get('organ', '')
                weight = data.get('weight', None)
                patientid = data.get('patientId', '')

                # Create a cursor object to interact with the database
                cursor = mydb.cursor()

                query = """
                    INSERT INTO user (
                        patientId, firstname, lastname, sex, marital, dob, organ, weight
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s
                    )
                """

                # Execute the query with the provided data
                cursor.execute(query, (
                    patientid, firstname, lastname, sex, marital_status, dob, organ, weight
                ))

                # Commit the changes to the database
                mydb.commit()

                # Close the cursor
                cursor.close()

                return jsonify({'message': 'User created successfully', 'patientid': patientid}), 201
            else:
                return jsonify({'error': 'Invalid form data format'}), 400
        except Exception as e:
            print(e)  # For debugging
            mydb.rollback()  # Roll back the transaction in case of an error
            return jsonify({'error': 'Failed to store data in the database'}), 500
            
@app.route('/add_lung_options', methods=['POST'])
def add_lung_options():
    if request.method == 'POST':
        patientid = None  # Define patientid at a higher scope
        try:
            data = request.get_json()
            if 'patientId' in data:
                patientid = data.get('patientId')

                # Create a cursor object to interact with the database
                cursor = mydb.cursor()

                # Check if the patient exists in the database
                cursor.execute("SELECT * FROM user WHERE patientid = %s", (patientid,))
                user = cursor.fetchone()

                if user:
                    # Update the user's lung options
                    update_query = """
                        UPDATE user
                        SET lungoptions = %s, chiefcomplaints = %s,
                            pastmedicalhistory = %s, substanceabuse = %s
                        WHERE patientid = %s
                    """
                    cursor.execute(update_query, (
                        data.get('lungOption', ''),
                        data.get('chiefOption', ''),
                        data.get('pastMedicalHistoryOption', ''),
                        data.get('substanceAbuseOption', ''),
                        patientid
                    ))

                    # Commit the changes to the database
                    mydb.commit()

                    # Close the cursor
                    cursor.close()

                    return jsonify({'message': 'Lung options added successfully', 'patientid': patientid}), 200
                else:
                    return jsonify({'error': 'Patient not found'}), 404
            else:
                return jsonify({'error': 'Invalid form data format'}), 400
        except Exception as e:
            print(e)  # For debugging
            mydb.rollback()
            return jsonify({'error': 'Failed to store lung options in the database'}), 500
            
@app.route('/third_block_option', methods=['POST'])
def third_block_option():
    if request.method == 'POST':
        patientid = None  # Define patientid at a higher scope
        try:
            data = request.get_json()
            if 'patientId' in data:
                patientid = data.get('patientId')

                # Create a cursor object to interact with the database
                cursor = mydb.cursor()

                # Check if the patient exists in the database
                cursor.execute("SELECT * FROM user WHERE patientid = %s", (patientid,))
                user = cursor.fetchone()

                if user:
                    # Update the user's lung options
                    update_query = """
                        UPDATE user
                        SET breathsound = %s, dbslaterality = %s,
                            dbslateralityoptionsopt = %s, crackleslaterality = %s,
                            crackleslateralityoptionsopt = %s, prlaterality = %s,
                            prlateralityoptionsopt = %s, rhonchilaterality = %s,
                            rhonchilateralityoptionsopt = %s, stridorlaterality = %s,
                            stridorlateralityoptionsopt = %s, wheezinglaterality = %s,
                            wheezinglateralityoptionsopt = %s, chestimaging = %s,
                            diagnosis = %s, resistancetboption = %s, mdrxdroption =%s, cnfdiagnosis = %s,
                            relapse = %s
                        WHERE patientid = %s
                    """
                    cursor.execute(update_query, (
                        data.get('breathSoundOption', ''), data.get('DbslateralityOption', ''),
                        data.get('DbslateralityOptionopt', ''), data.get('CrackleslateralityOption', ''),
                        data.get('CrackleslateralityOptionopt', ''), data.get('PrlateralityOption', ''),
                        data.get('PrlateralityOptionopt', ''), data.get('RhonchilateralityOption', ''),
                        data.get('RhonchilateralityOptionopt', ''), data.get('StridorlateralityOption', ''),
                        data.get('StridorlateralityOptionopt', ''), data.get('WheezinglateralityOption', ''),
                        data.get('WheezinglateralityOptionopt', ''), data.get('imagingOption', ''),
                        data.get('diagnosisOption', ''), data.get('resistancetb', ''), data.get('mdrxdrtb', ''),
                        data.get('cnfdiagnosisOption', ''), data.get('relapseChoice', ''), patientid
                    ))

                    # Commit the changes to the database
                    mydb.commit()

                    # Close the cursor
                    cursor.close()

                    return jsonify({'message': 'Breath sound added successfully', 'patientid': patientid}), 200
                else:
                    return jsonify({'error': 'Patient not found'}), 404
            else:
                return jsonify({'error': 'Invalid form data format'}), 400
        except Exception as e:
            print(e)  # For debugging
            mydb.rollback()
            return jsonify({'error': 'Failed to store breath sound in the database'}), 500

@app.route('/fourth_block_option', methods=['POST'])
def fourth_block_option():
    if request.method == 'POST':
        patientid = None  # Define patientid at a higher scope
        try:
            data = request.get_json()
            if 'patientId' in data:
                patientid = data.get('patientId')

                # Create a cursor object to interact with the database
                cursor = mydb.cursor()

                # Check if the patient exists in the database
                cursor.execute("SELECT * FROM user WHERE patientid = %s", (patientid,))
                user = cursor.fetchone()

                if user:
                    # Update the user's lung options
                    update_query = """
                        UPDATE user
                        SET pastsurgicalhistoryoption = %s,
                            respiratorysystemoption = %s,
                            cardiovascularsystemoption = %s,
                            renalsystemoption = %s
                        WHERE patientid = %s
                    """
                    cursor.execute(update_query, (
                        data.get('pastSurgicalHistoryOption', ''),
                        data.get('respiratorySystemOption', ''),
                        data.get('cardiovascularSystemOption', ''),
                        data.get('renalSystemOption', ''),
                        patientid
                    ))

                    # Commit the changes to the database
                    mydb.commit()

                    # Close the cursor
                    cursor.close()

                    return jsonify({'message': 'Options added successfully', 'patientid': patientid}), 200
                else:
                    return jsonify({'error': 'Patient not found'}), 404
            else:
                return jsonify({'error': 'Invalid form data format'}), 400
        except Exception as e:
            print(e)  # For debugging
            mydb.rollback()
            return jsonify({'error': 'Failed to store options in the database'}), 500
            
@app.route('/currentmedication_block_option', methods=['POST'])
def currentmedication_block_option():
    if request.method == 'POST':
        patientid = None  # Define patientid at a higher scope
        try:
            data = request.get_json()
            if 'patientId' in data:
                patientid = data.get('patientId')

                # Create a cursor object to interact with the database
                cursor = mydb.cursor()

                # Check if the patient exists in the database
                cursor.execute("SELECT * FROM user WHERE patientid = %s", (patientid,))
                user = cursor.fetchone()

                if user:
                    # Update the user's lung options
                    update_query = """
                        UPDATE user
                        SET currentmedicationsoption = %s
                        WHERE patientid = %s
                    """
                    cursor.execute(update_query, (
                        data.get('CurrentMedicationsOption', ''),
                        patientid
                    ))

                    # Commit the changes to the database
                    mydb.commit()

                    # Close the cursor
                    cursor.close()

                    return jsonify({'message': 'Options added successfully', 'patientid': patientid}), 200
                else:
                    return jsonify({'error': 'Patient not found'}), 404
            else:
                return jsonify({'error': 'Invalid form data format'}), 400
        except Exception as e:
            print(e)  # For debugging
            mydb.rollback()
            return jsonify({'error': 'Failed to store options in the database'}), 500 
@app.route('/fifth_block_option', methods=['POST'])
def fifth_block_option():
    if request.method == 'POST':
        patientid = None  # Define patientid at a higher scope
        try:
            data = request.get_json()
            if 'patientId' in data:
                patientid = data.get('patientId')

                # Create a cursor object to interact with the database
                cursor = mydb.cursor()

                # Check if the patient exists in the database
                cursor.execute("SELECT * FROM user WHERE patientid = %s", (patientid,))
                user = cursor.fetchone()

                if user:
                    # Update the user's lung options
                    update_query = """
                        UPDATE user
                        SET adversereaction = %s
                        WHERE patientid = %s
                    """
                    cursor.execute(update_query, (
                        data.get('adverseReactionOption', ''),
                        patientid
                    ))

                    # Commit the changes to the database
                    mydb.commit()

                    # Close the cursor
                    cursor.close()

                    return jsonify({'message': 'Options added successfully', 'patientid': patientid}), 200
                else:
                    return jsonify({'error': 'Patient not found'}), 404
            else:
                return jsonify({'error': 'Invalid form data format'}), 400
        except Exception as e:
            print(e)  # For debugging
            mydb.rollback()
            return jsonify({'error': 'Failed to store options in the database'}), 500
            
@app.route('/get_user_data', methods=['GET'])
def get_user_data():
    try:
        patient_id = request.args.get('patient_id')

     

        # Create a cursor object to interact with the database
        cursor = mydb.cursor(dictionary=True)  # Set dictionary=True to get a dictionary instead of a tuple

        # Check if the patient exists in the database
        cursor.execute("SELECT * FROM user WHERE patientid = %s", (patient_id,))
        user = cursor.fetchone()

        # Close the cursor and MySQL connection
        cursor.close()

        if user:
            user_data = {
                'firstname': user['firstname'],
                'lastname': user['lastname'],'sex': user['sex'],
                'weight': user['weight'],
                'marital': user['marital'],
                'dob': user['dob'],
                'organ': user['organ'],
                'lungoption': user['lungoptions'],
                'chiefcomplaints': user['chiefcomplaints'],
                'pastmedicalhistory': user['pastmedicalhistory'],
                'substanceabuse': user['substanceabuse'],
                'breathsound': user['breathsound'],
                'dbslaterality': user['dbslaterality'],
                'dbslateralityoptionsopt': user['dbslateralityoptionsopt'],
                'crackleslaterality': user['crackleslaterality'],
                'crackleslateralityoptionsopt': user['crackleslateralityoptionsopt'],
                'prlaterality': user['prlaterality'],
                'prlateralityoptionsopt': user['prlateralityoptionsopt'],
                'rhonchilaterality': user['rhonchilaterality'],
                'rhonchilateralityoptionsopt': user['rhonchilateralityoptionsopt'],
                'stridorlaterality': user['stridorlaterality'],
                'stridorlateralityoptionsopt': user['stridorlateralityoptionsopt'],
                'wheezinglaterality': user['wheezinglaterality'],
                'wheezinglateralityoptionsopt': user['wheezinglateralityoptionsopt'],
                'chestimaging': user['chestimaging'],
                'diagnosis': user['diagnosis'],
                'resistancetboption': user['resistancetboption'],
                'mdrxdroption': user['mdrxdroption'],
                'cnfdiagnosis': user['cnfdiagnosis'],
                'relapse': user['relapse'],
                'pastsurgicalhistoryoption': user['pastsurgicalhistoryoption'],
                'respiratorysystemoption': user['respiratorysystemoption'],
                'cardiovascularsystemoption': user['cardiovascularsystemoption'],
                'renalsystemoption': user['renalsystemoption'],
                'currentmedicationsoption': user['currentmedicationsoption'],
                'adversereaction': user['adversereaction'],
                'created_at': user['created_at'] if isinstance(user['created_at'], str) else user['created_at'].strftime('%Y-%m-%d %H:%M:%S'),
                # Add more fields as needed
                # Add other fields as needed
            }
            return jsonify(user_data)
        return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        # Log the error for debugging
        print(f"Error in get_user_data: {str(e)}")
        return jsonify({'error': 'An error occurred'}), 500
        
@app.route('/patient/data', methods=['GET'])
def get_patient_data():
    try:
        

        # Create a cursor object to interact with the database
        cursor = mydb.cursor(dictionary=True)

        # Execute the query to fetch patient data
        query = "SELECT patientid, firstname, lastname, organ FROM user"
        cursor.execute(query)

        # Fetch all the rows as a list of dictionaries
        patients = cursor.fetchall()

        # Convert the query result to the desired format
        patient_data = [
            {
                'patientId': patient['patientid'],
                'firstName': patient['firstname'],
                'lastName': patient['lastname'],
                'organ': patient['organ']
            }
            for patient in patients
        ]

        # Close the cursor and connection
        cursor.close()

        return jsonify({'patientData': patient_data})

    except Exception as e:
        # Log the error for debugging
        print(f"Error in get_patient_data: {str(e)}")
        return jsonify({'error': 'An error occurred while fetching patient data'}), 500

@app.route('/patient/count', methods=['GET'])
def get_patient_count():
    database = None

    try:
        # Connect to the MySQL database
        database = mysql.connector.connect(
            host="184.168.97.94",
            user="Shenmedical",
            password="Satyam@9931",
            database="raj_shenmedical_12"
        )

        print("Connected to the database")

        # Query the database for the total number of patients
        total_patients_query = "SELECT COUNT(*) FROM user"
        total_patients_count = execute_query(database, total_patients_query)

        # Query the database for the total number of patients for lungs
        lungs_query = "SELECT COUNT(*) FROM user WHERE organ = 'Lungs'"
        lungs_count = execute_query(database, lungs_query)

        # Query the database for the total number of patients for brains
        brains_query = "SELECT COUNT(*) FROM user WHERE organ = 'Brain'"
        brains_count = execute_query(database, brains_query)

        return jsonify({
            'total_patients_count': total_patients_count,
            'lungs_count': lungs_count,
            'brains_count': brains_count
        })

    except Exception as e:
        print("Error:", e)
        return jsonify({'error': str(e)})

    finally:
        if database:
            database.close()

# Function to execute a query and fetch the result
def execute_query(database, query):
    cursor = database.cursor(dictionary=True)

    try:
        cursor.execute(query)
        result = cursor.fetchall()
        print("Executed query:", query)
        print("Query result:", result)

        # Check if the result is not empty
        if result and result[0]:
            # Return the first column of the first row
            return result[0][next(iter(result[0]))]

        # Return None if the result is empty
        return None

    except Exception as e:
        print("Error executing query:", e)
        return None

    finally:
        cursor.close()


if __name__ == '__main__':
    app.run(debug=False)  # Specify the port to avoid CORS issues
    
