from flask import Flask, current_app, request, jsonify, session
from flask_cors import CORS
from models import User, Login
from user_routes import user_routes
from lung_options_routes import lung_options_routes
from third_block_routes import third_block_routes
from fourth_block_routes import fourth_block_routes
from fifth_block_routes import fifth_block_routes
from currentmedication_block_routes import currentmedication_block_routes
from api_routes import api_routes
from patient_data_routes import patient_data_routes
from patient_count_routes import patient_count_routes
import mysql.connector
from utils import execute_query
app = Flask(__name__)
CORS(app, origins=['http://localhost:3000'])

# Initialize the Flask session
app.secret_key = 's9a9t3y1a4m8k8u7m5a7r'  # Change 'your_secret_key' to a secure, random string

# MySQL configuration (update with your actual MySQL database details)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/raj'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://Shenmedical:Satyam@9931@184.168.97.94/raj_shenmedical_12'
mydb = mysql.connector.connect(
    host="184.168.97.94",
    username="Shenmedical",
    password = "Satyam@9931",
    database="raj_shenmedical_12"
)
print(mydb)

app.register_blueprint(user_routes)
app.register_blueprint(lung_options_routes)
app.register_blueprint(third_block_routes)
app.register_blueprint(fourth_block_routes)
app.register_blueprint(fifth_block_routes)
app.register_blueprint(currentmedication_block_routes)
app.register_blueprint(api_routes)
app.register_blueprint(patient_data_routes)
app.register_blueprint(patient_count_routes)
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Use a cursor to execute the query
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



if __name__ == '__main__':
    app.run(debug=True)
