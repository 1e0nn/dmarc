import os
import zipfile
import gzip
import shutil

def extract_zip_files(source_directory, destination_directory):
    """
    Extracts all .zip files from the source_directory and places the extracted files in the destination_directory.
    
    :param source_directory: Directory containing the .zip files.
    :param destination_directory: Directory where the extracted files will be placed.
    """
    # Iterate over all files in the source directory
    for filename in os.listdir(source_directory):
        if filename.endswith('.zip'):
            source_path = os.path.join(source_directory, filename)
            with zipfile.ZipFile(source_path, 'r') as zip_ref:
                zip_ref.extractall(destination_directory)
                print(f'Extracted: {source_path} to {destination_directory}')

def extract_gz_files(source_directory, destination_directory):
    """
    Extracts all .gz files from the source_directory and places the extracted files in the destination_directory.
    
    :param source_directory: Directory containing the .gz files.
    :param destination_directory: Directory where the extracted files will be placed.
    """
    # Iterate over all files in the source directory
    for filename in os.listdir(source_directory):
        if filename.endswith('.gz'):
            source_path = os.path.join(source_directory, filename)
            destination_path = os.path.join(destination_directory, filename[:-3])  # Remove the .gz extension
            
            with gzip.open(source_path, 'rb') as f_in:
                with open(destination_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
                    
            print(f'Extracted: {source_path} to {destination_path}')

def main():
    source_directory = r'C:\Users\test\path\source'
    destination_directory = r'C:\Users\test\path\dest'

    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)

    extract_zip_files(source_directory, destination_directory)
    extract_gz_files(source_directory, destination_directory)

if __name__ == "__main__":
    main()
