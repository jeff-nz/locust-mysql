from locust import User, task, between
import mysql.connector
import random

# Define random values to use in the database insert
random_values = [
    ("Alice", "alice@example.com", 25),
    ("Bob", "bob@example.com", 30),
    ("Charlie", "charlie@example.com", 35),
    ("David", "david@example.com", 40),
]

class MySQLUser(User):
    # Define wait time between tasks
    wait_time = between(1, 3)

    def on_start(self):
        """
        This method is called when a Locust user starts.
        """
        # Initialize MySQL connection
        self.connection = mysql.connector.connect(
            host="your_mysql_host",
            user="your_mysql_user",
            password="your_mysql_password",
            database="your_database"
        )
        self.cursor = self.connection.cursor()

    @task
    def insert_into_db(self):
        # Select a random value from the list
        random_data = random.choice(random_values)
        # Insert the random data into the database
        try:
            self.cursor.execute(
                "INSERT INTO your_table_name (name, email, age) VALUES (%s, %s, %s)",
                random_data
            )
            self.connection.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def on_stop(self):
        """
        This method is called when a Locust user stops.
        """
        # Close the cursor and connection
        self.cursor.close()
        self.connection.close()
