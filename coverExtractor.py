import os
from pdf2image import convert_from_path
from PIL import Image

class CoverExtractor:
    def __init__(self, download_dir="downloaded_books"):
        self.download_dir = download_dir
        self.cover_filename = "cover.jpg"

    def extract_cover(self, pdf_file, output_folder):
        try:
            # Convert the first page of the PDF to an image
            images = convert_from_path(pdf_file, first_page=1, last_page=1)
            if images:
                cover_image_path = os.path.join(output_folder, self.cover_filename)
                images[0].save(cover_image_path, 'JPEG')
                print(f"Saved cover image for {pdf_file} to {cover_image_path}")
            else:
                print(f"Failed to extract cover from {pdf_file}")
        except Exception as e:
            print(f"Error extracting cover from {pdf_file}: {str(e)}")

    def process_folders(self):
        # Iterate through each folder in the download directory
        for folder in os.listdir(self.download_dir):
            folder_path = os.path.join(self.download_dir, folder)
            if os.path.isdir(folder_path):
                # Find the PDF file in the folder
                pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
                if pdf_files:
                    pdf_file_path = os.path.join(folder_path, pdf_files[0])
                    self.extract_cover(pdf_file_path, folder_path)

if __name__ == "__main__":
    extractor = CoverExtractor()
    extractor.process_folders()
