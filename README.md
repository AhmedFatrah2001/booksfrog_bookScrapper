
---

# Book Scraper and Cover Extractor

This project includes two Python scripts: `BookScraper` for scraping and downloading books, and `coverExtractor` for extracting the cover page from each book's PDF file. The project connects to a MySQL database to store book metadata such as title, author, summary, and PDF content.

## Features

- **BookScraper**:
  - Downloads books and metadata (author and description) from the website.
  - Stores the downloaded books in a folder structure, each folder representing a book.
  - Saves the book's PDF, author, and description inside the folder.

- **CoverExtractor**:
  - Extracts the first page (cover) from each PDF in the `downloaded_books` folder.
  - Saves the extracted cover as `cover.jpg` inside each book's folder.

- **Database Inserter**:
  - Connects to a MySQL database.
  - Inserts book details including the title, author, description, cover image, and the PDF content.

## Prerequisites

Before running the scripts, ensure you have the following:

1. Python 3.x installed.
2. A virtual environment (optional but recommended).
3. Required Python packages installed (see **Installation** below).
4. MySQL database up and running.

### Environment Variables

You'll need to set up the `.env` file with the following format for the MySQL connection:

```
DB_HOST=localhost
DB_PORT=3306
DB_NAME=booksfrog
DB_USER=root
DB_PASSWORD=Ahmed159263
```

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/book-scraper.git
    cd book-scraper
    ```

2. (Optional) Set up a virtual environment:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up your MySQL database as per the `.env` file and ensure it's running.

## Usage

### 1. BookScraper Script

This script scrapes books from the website and saves them to the `downloaded_books` folder.

To run the book scraper:

```bash
python book_scraper.py
```

The scraper will download books, save the PDFs, authors, and descriptions, and place each book inside its folder under `downloaded_books`.

### 2. CoverExtractor Script

This script extracts the first page (cover) from each book's PDF in the `downloaded_books` folder and saves it as `cover.jpg` inside each respective folder.

To run the cover extractor:

```bash
python cover_extractor.py
```

### 3. Insert Books to Database

The `insert_books.py` script reads the contents of each folder in `downloaded_books`, extracts the author, description, and cover image, and uploads this data to the MySQL database.

To run the script:

```bash
python insert_books.py
```

This script will automatically skip over missing files (e.g., missing cover images or PDFs) and continue processing the rest of the books.

## Error Handling

- If any of the files (author, description, or cover image) are missing in a folder, the script will skip them and move on to the next folder.
- After processing all folders, the script will print out any missing files or errors that occurred during the process.
