import mysql.connector
from mysql.connector import Error

# Function to create a MySQL connection
def create_connection():
    try:
        connection = mysql.connector.connect(
             host="184.168.97.94",
    	     username="Shenmedical",
       	     password = "Satyam@9931",
    	     database="raj_shenmedical_12"
        )
        if connection.is_connected():
            print("Connected to MySQL database")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

# Function to execute a query
def execute_query(connection, query):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()

# Function to create the 'user' table
def User(connection):
    query = """
    CREATE TABLE IF NOT EXISTS user (
    sno INT AUTO_INCREMENT PRIMARY KEY,
    patientid VARCHAR(100) UNIQUE NOT NULL,
    firstname VARCHAR(255) NOT NULL,
    lastname VARCHAR(255) NOT NULL,
    sex VARCHAR(10),
    marital VARCHAR(20),
    dob DATE,
    organ VARCHAR(20),
    weight FLOAT,
    lungoptions VARCHAR(250),
    chiefcomplaints VARCHAR(250),
    pastmedicalhistory VARCHAR(250),
    substanceabuse VARCHAR(250),
    breathsound VARCHAR(250),
    dbslaterality VARCHAR(250),
    dbslateralityoptionsopt VARCHAR(250),
    bbslaterality VARCHAR(250),
    bbslateralityoptionsopt VARCHAR(250),
    crackleslaterality VARCHAR(250),
    crackleslateralityoptionsopt VARCHAR(250),
    prlaterality VARCHAR(250),
    prlateralityoptionsopt VARCHAR(250),
    rhonchilaterality VARCHAR(250),
    rhonchilateralityoptionsopt VARCHAR(250),
    stridorlaterality VARCHAR(250),
    stridorlateralityoptionsopt VARCHAR(250),
    wheezinglaterality VARCHAR(250),
    wheezinglateralityoptionsopt VARCHAR(250),
    chestimaging VARCHAR(250),
    diagnosis VARCHAR(250),
    resistancetboption VARCHAR(250),
    cnfdiagnosis VARCHAR(250),
    relapse VARCHAR(250),
    pastsurgicalhistoryoption VARCHAR(250),
    respiratorysystemoption VARCHAR(250),
    cardiovascularsystemoption VARCHAR(250),
    renalsystemoption VARCHAR(250),
    currentmedicationsoption VARCHAR(250),
    adversereaction VARCHAR(250),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
    """
    execute_query(connection, query)

# Function to create the 'login' table
def Login(connection):
    query = """
    CREATE TABLE IF NOT EXISTS login (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(250) UNIQUE NOT NULL,
    password VARCHAR(250) NOT NULL,
    name VARCHAR(250) NOT NULL,
    profession VARCHAR(250) NOT NULL
);
    """
    execute_query(connection, query)

# Call the create_connection function to get a connection
conn = create_connection()

# Check if the connection is successful before creating tables
if conn:
    # Create 'user' table
    User(conn)

    # Create 'login' table
    Login(conn)

    # Close the connection when done
    conn.close()
