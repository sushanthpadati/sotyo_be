from flask import Blueprint, jsonify
from utils import execute_query
import mysql.connector

patient_count_routes = Blueprint('patient_count_routes', __name__)

@patient_count_routes.route('/patient/count', methods=['GET'])
def get_patient_count():
    database = None

    try:
        database = mysql.connector.connect(
           host="184.168.97.94",
    username="Shenmedical",
    password = "Satyam@9931",
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
