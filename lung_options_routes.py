from flask import Blueprint, request, jsonify
import mysql.connector

# Assuming you have the MySQL connection details
mydb = mysql.connector.connect(
    host="184.168.97.94",
    username="Shenmedical",
    password="Satyam@9931",
    database="raj_shenmedical_12"
)

lung_options_routes = Blueprint('lung_options_routes', __name__)

@lung_options_routes.route('/add_lung_options', methods=['POST'])
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
