import mysql.connector

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
