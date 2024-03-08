# api_routes.py
from flask import Blueprint, jsonify, request
import mysql.connector

api_routes = Blueprint('api_routes', __name__)

@api_routes.route('/get_user_data', methods=['GET'])
def get_user_data():
    try:
        patient_id = request.args.get('patient_id')

        # Assuming you have the MySQL connection details
        mydb = mysql.connector.connect(
            host="184.168.97.94",
            username="Shenmedical",
            password="Satyam@9931",
            database="raj_shenmedical_12"
        )

        # Create a cursor object to interact with the database
        cursor = mydb.cursor(dictionary=True)  # Set dictionary=True to get a dictionary instead of a tuple

        # Check if the patient exists in the database
        cursor.execute("SELECT * FROM user WHERE patientid = %s", (patient_id,))
        user = cursor.fetchone()

        # Close the cursor and MySQL connection
        cursor.close()
        mydb.close()

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
