from locust import User, task, between, events
import mysql.connector
from mysql.connector import Error
import random
import time
import logging
import string

# Set up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define random values to use in the database insert
random_values = [
    ("Alice", "alice@example.com"),
    ("Bob", "bob@example.com"),
    ("Charlie", "charlie@example.com"),
    ("David", "david@example.com"),
]

class MySQLInsertError(Exception):
    """Custom exception for MySQL insert errors."""
    def __init__(self, message):
        super().__init__(message)

class MySQLUser(User):
    # Define wait time between tasks
    wait_time = between(1, 3)
    connection = None
    cursor = None
    def on_start(self):
        logging.info(f"Running on_start definitions...")
        try:
            # Initialize MySQL connection
            self.connection = mysql.connector.connect(
                host="127.0.0.1",
                user="locust-mysql-user",
                password="my_cool_secret",
                database="test"
            )
            self.cursor = self.connection.cursor()
            logger.info("Connected to MySQL successfully.")
        except Error as e:
            logger.error(f"Error connecting to MySQL: {e}")
            self.environment.runner.quit()

    def on_stop(self):
        logger.info(f"Running on_stop definitions...")

        if self.connection is None:
            return None

        # Close the cursor and connection
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()

    @task
    def insert_into_db(self):
        start_time = time.time()  # Start measuring time before the operation

        if self.cursor is None:
            return None

        # Select a random value from the list
        # random_data = random.choice(random_values)

        age = random.randint(16, 99)
        random_data = [self.generate_random_name(), self.generate_random_email()]
        # Insert the random data into the database
        try:
            #use from array of random data
            # self.cursor.execute(
            #     f"INSERT INTO users (id, name, email, age) VALUES (UUID(), %s, %s, {age})",
            #     random_data
            # )

            self.cursor.execute(
                f"INSERT INTO users (id, name, email, age) VALUES (UUID(), %s, %s, {age})",
                random_data
            )
            self.connection.commit()
            response_time = (time.time() - start_time) * 1000  # Calculate response time in milliseconds
            response_length = 0  # Calculate response length as the length of the query string
            # If no error occurs, signal a success to Locust
            events.request.fire(
                request_type="MySQL",
                name="insert_into_mysql",
                response_time=response_time,
                response_length=response_length,
                exception=None
            )
        except mysql.connector.Error as e:
            logger.error(f"Error during MySQL insert: {e}")
            response_time = (time.time() - start_time) * 1000  # Calculate response time in milliseconds
            response_length = 0  # Calculate response length as the length of the query string
            events.request.fire(
                request_type="MySQL",
                name="insert_into_mysql",
                response_time=response_time,
                response_length=response_length,
                exception=e
            )

    def generate_random_email(self):
        # Define the length of the username and domain parts
        username_length = 8
        domain_length = 5

        # Generate a random username
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=username_length))

        # Generate a random domain
        domain = ''.join(random.choices(string.ascii_lowercase, k=domain_length))

        # Define a list of common top-level domains (TLDs)
        tlds = ['com', 'org', 'net', 'edu', 'gov']

        # Choose a random TLD
        tld = random.choice(tlds)

        # Combine the parts into an email address
        email = f"{username}@{domain}.{tld}"
        return email

    def generate_random_name(self):
        first_names = ['Alice', 'Bob', 'Charlie', 'David', 'Eva', 'Fiona', 'George', 'Hannah']
        last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis']

        first_name = random.choice(first_names)
        last_name = random.choice(last_names)

        return f"{first_name} {last_name}"
