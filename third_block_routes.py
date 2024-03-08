from flask import Blueprint, request, jsonify
import mysql.connector

# Assuming you have the MySQL connection details
mydb = mysql.connector.connect(
    host="184.168.97.94",
    username="Shenmedical",
    password="Satyam@9931",
    database="raj_shenmedical_12"
)

third_block_routes = Blueprint('third_block_routes', __name__)

@third_block_routes.route('/third_block_option', methods=['POST'])
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
                            diagnosis = %s, resistancetboption = %s, cnfdiagnosis = %s,
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
                        data.get('diagnosisOption', ''), data.get('resistancetb', ''),
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
