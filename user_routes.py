from flask import Blueprint, request, jsonify
import mysql.connector

# Assuming you have the MySQL connection details
mydb = mysql.connector.connect(
    host="184.168.97.94",
    username="Shenmedical",
    password="Satyam@9931",
    database="raj_shenmedical_12"
)

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/add', methods=['POST'])
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
