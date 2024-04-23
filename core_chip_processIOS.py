import os
import console
import zipfile
import hashlib
import shutil
import tempfile
import base64
import concurrent.futures
import boto3
from cryptography.fernet import Fernet

class IOSFileProcessor:
    def __init__(self):
        self.s3_client = boto3.client('s3')
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)
        self.fernet_key = Fernet.generate_key()
        self.fernet_cipher = Fernet(self.fernet_key)

    def process_files(self, directory):
        try:
            files = self.get_files_in_directory(directory)
            if not files:
                console.alert("Error", "No files found in the specified directory.", "OK", hide_cancel_button=True)
                return

            for file_path in files:
                self.executor.submit(self.process_file, file_path)

            console.hud_alert("Processing complete", "success", duration=2)
        except Exception as e:
            console.alert("Error", f"An error occurred: {str(e)}", "OK", hide_cancel_button=True)

    def process_file(self, file_path):
        try:
            # Example processing: Compress and encrypt file
            temp_dir = tempfile.mkdtemp()
            temp_zip_path = os.path.join(temp_dir, "compressed_file.zip")
            self.compress_file(file_path, temp_zip_path)
            encrypted_zip_path = self.encrypt_file(temp_zip_path)
            self.upload_to_s3(encrypted_zip_path)
            console.hud_alert(f"Processed and uploaded file: {os.path.basename(file_path)}", "success", duration=1)
        except Exception as e:
            raise RuntimeError(f"Error processing file {file_path}: {str(e)}")

    def compress_file(self, file_path, output_path):
        with zipfile.ZipFile(output_path, 'w') as zipf:
            zipf.write(file_path, arcname=os.path.basename(file_path))

    def encrypt_file(self, file_path):
        with open(file_path, 'rb') as f:
            data = f.read()
        hashed_data = hashlib.sha256(data).digest()
        encrypted_data = self.fernet_cipher.encrypt(hashed_data)
        encrypted_file_path = file_path + '.enc'
        with open(encrypted_file_path, 'wb') as f:
            f.write(encrypted_data)
        return encrypted_file_path

    def get_files_in_directory(self, directory):
        files = []
        for root, _, filenames in os.walk(directory):
            for filename in filenames:
                file_path = os.path.join(root, filename)
                files.append(file_path)
        return files

    def upload_to_s3(self, file_path):
        bucket_name = 'your-bucket-name'
        key = os.path.basename(file_path)
        self.s3_client.upload_file(file_path, bucket_name, key)

def main():
    file_processor = IOSFileProcessor()

    # Prompt user for directory
    directory = console.input_alert("Enter Directory", "Enter the directory path:", "", "OK", hide_cancel_button=True)

    # Process files in the specified directory
    file_processor.process_files(directory)

if __name__ == "__main__":
    main()
