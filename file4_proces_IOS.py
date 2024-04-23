import ui
import os
import console
import clipboard
import threading
import mimetypes
import concurrent.futures
import boto3

class IOSFileProcessor:
    def __init__(self):
        self.files_processed = 0

    def process_files(self, directory, file_extension=None):
        try:
            files = self.get_files_in_directory(directory, file_extension)
            if not files:
                console.alert("Error", "No files found in the specified directory.", "OK", hide_cancel_button=True)
                return

            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = [executor.submit(self.process_file, file_path) for file_path in files]

                for future in concurrent.futures.as_completed(futures):
                    try:
                        future.result()
                        self.files_processed += 1
                    except Exception as e:
                        console.alert("Error", f"An error occurred: {str(e)}", "OK", hide_cancel_button=True)

            self.display_summary()
        except Exception as e:
            console.alert("Error", f"An error occurred: {str(e)}", "OK", hide_cancel_button=True)

    def process_file(self, file_path):
        try:
            with open(file_path, "r") as file:
                content = file.read()
                # Perform processing tasks here
                processed_content = self.process_content(content)
                # Save processed content to clipboard
                clipboard.set(processed_content)
                console.hud_alert(f"Processed and copied content of {os.path.basename(file_path)} to clipboard", "success", duration=2)
        except Exception as e:
            raise RuntimeError(f"Error processing file {file_path}: {str(e)}")

    def process_content(self, content):
        # Example processing: Convert content to uppercase
        return content.upper()

    def display_summary(self):
        console.alert("Processing Complete", f"Processed {self.files_processed} files", "OK", hide_cancel_button=True)

    def get_files_in_directory(self, directory, file_extension=None):
        files = []
        for root, _, filenames in os.walk(directory):
            for filename in filenames:
                file_path = os.path.join(root, filename)
                if not file_extension or filename.endswith(file_extension):
                    files.append(file_path)
        return files

def main():
    file_processor = IOSFileProcessor()

    # Prompt user for directory and file extension
    directory = console.input_alert("Enter Directory", "Enter the directory path:", "", "OK", hide_cancel_button=True)
    file_extension = console.input_alert("Enter File Extension", "Enter the file extension (e.g., .txt):", "", "OK", hide_cancel_button=True)

    # Process files in the specified directory
    file_processor.process_files(directory, file_extension)

if __name__ == "__main__":
    main()
