# file_processor.py

import os
import shutil
import threading
import logging

class FileProcessor:
    def __init__(self):
        self.logger = self.setup_logger()

    def setup_logger(self):
        logger = logging.getLogger("FileProcessor")
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        return logger

    def read_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                data = file.read()
                return data
        except Exception as e:
            self.logger.error(f"Error reading file {file_path}: {e}")
            return None

    def write_file(self, file_path, data):
        try:
            with open(file_path, 'w') as file:
                file.write(data)
        except Exception as e:
            self.logger.error(f"Error writing file {file_path}: {e}")

    def copy_file(self, source_path, destination_path):
        try:
            shutil.copyfile(source_path, destination_path)
        except Exception as e:
            self.logger.error(f"Error copying file from {source_path} to {destination_path}: {e}")

    def move_file(self, source_path, destination_path):
        try:
            shutil.move(source_path, destination_path)
        except Exception as e:
            self.logger.error(f"Error moving file from {source_path} to {destination_path}: {e}")

    def delete_file(self, file_path):
        try:
            os.remove(file_path)
        except Exception as e:
            self.logger.error(f"Error deleting file {file_path}: {e}")

    def process_files_background(self, files):
        thread = threading.Thread(target=self.process_files, args=(files,))
        thread.daemon = True
        thread.start()

    def process_files(self, files):
        self.logger.info("Processing files...")
        for file in files:
            data = self.read_file(file)
            if data:
                processed_data = data.upper()  # Placeholder processing
                processed_file_path = f"processed_{os.path.basename(file)}"
                self.write_file(processed_file_path, processed_data)
                self.copy_file(processed_file_path, f"copied_{processed_file_path}")
                self.move_file(f"copied_{processed_file_path}", f"destination/{os.path.basename(file)}")
                self.delete_file(processed_file_path)
                self.logger.info(f"File {os.path.basename(file)} processed and moved to destination folder")

if __name__ == "__main__":
    file_processor = FileProcessor()
    files_to_process = ["file1.txt", "file2.txt", "file3.txt"]  # Example list of files to process
    file_processor.process_files_background(files_to_process)
