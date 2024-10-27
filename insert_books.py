import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

class BookInserter:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()
        self.db_config = {
            'host': os.getenv('DB_HOST'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
            'database': os.getenv('DB_NAME'),
            'port': os.getenv('DB_PORT', 3306)
        }
        self.download_dir = "downloaded_books"
        self.missing_files = []

    def connect(self):
        try:
            connection = mysql.connector.connect(**self.db_config)
            if connection.is_connected():
                print("Connected to MySQL database")
                return connection
        except Error as e:
            print(f"Error: {e}")
            return None

    def read_file(self, file_path):
        try:
            with open(file_path, 'rb') as file:
                return file.read()
        except FileNotFoundError:
            self.missing_files.append(file_path)
            return None

    def read_text_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read().strip()
        except FileNotFoundError:
            self.missing_files.append(file_path)
            return None

    def insert_book(self, connection, title, author, content, cover, summary):
        try:
            cursor = connection.cursor()
            query = """INSERT INTO book (title, author, content, cover, summary) 
                    VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(query, (title, author, content, cover, summary))
            connection.commit()
            print(f"Inserted book '{title}' into database.")
        except Error as e:
            # Check if the error is related to max_allowed_packet size
            if "max_allowed_packet" in str(e):
                print(f"Error inserting book '{title}': {e}. The packet size might be too large.")
            else:
                print(f"Error inserting book '{title}': {e}")


    def process_folders(self):
        connection = self.connect()
        if connection is None:
            print("Failed to connect to the database.")
            return

        # Iterate through folders in the downloaded_books directory
        for folder in os.listdir(self.download_dir):
            folder_path = os.path.join(self.download_dir, folder)
            if os.path.isdir(folder_path):
                # Get book details from files
                title = folder
                author = self.read_text_file(os.path.join(folder_path, 'author.txt')) or 'Unknown Author'
                summary = self.read_text_file(os.path.join(folder_path, 'description.txt')) or 'No description available'
                content = self.read_file(os.path.join(folder_path, f"{folder}.pdf")) or None
                cover = self.read_file(os.path.join(folder_path, 'cover.jpg')) or None

                # Insert the book into the database
                self.insert_book(connection, title, author, content, cover, summary)

        connection.close()

        # Print missing files summary
        if self.missing_files:
            print("\nMissing files:")
            for missing_file in self.missing_files:
                print(missing_file)
        else:
            print("\nAll files were processed successfully!")

if __name__ == "__main__":
    inserter = BookInserter()
    inserter.process_folders()
