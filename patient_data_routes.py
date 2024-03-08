# Import necessary libraries
from flask import Blueprint, jsonify
import mysql.connector

# Create a new blueprint for the patient data
patient_data_routes = Blueprint('patient_data_routes', __name__)

# Route to get patient data
@patient_data_routes.route('/patient/data', methods=['GET'])
def get_patient_data():
    try:
        # Connect to the MySQL database
        connection = mysql.connector.connect(
            host="184.168.97.94",
    username="Shenmedical",
    password = "Satyam@9931",
    database="raj_shenmedical_12"
        )

        # Create a cursor object to interact with the database
        cursor = connection.cursor(dictionary=True)

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
        connection.close()

        return jsonify({'patientData': patient_data})

    except Exception as e:
        return jsonify({'error': str(e)})
