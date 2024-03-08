from flask import Blueprint, request, jsonify
import mysql.connector

# Assuming you have the MySQL connection details
mydb = mysql.connector.connect(
    host="184.168.97.94",
    username="Shenmedical",
    password="Satyam@9931",
    database="raj_shenmedical_12"
)

fourth_block_routes = Blueprint('fourth_block_routes', __name__)

@fourth_block_routes.route('/fourth_block_option', methods=['POST'])
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
