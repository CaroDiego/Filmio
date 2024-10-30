import argparse
import shutil
import zipfile

from FilmioBack.logger_config import lbox_logger


class ZipHandler:
    """
    Class to handle zip files operations, such as validation, extraction and backups.
    Attributes:
        temp_dir: str
            Temp directory to extract the zip file content..
        backup_dir: str
            Backup directory to store the zip files
    """

    def __init__(self, temp_dir='Data/Temp', backup_dir='Data/Backup'):
        self.temp_dir = temp_dir
        self.backup_dir = backup_dir

    def zip_file(self, path):
        """
        Validate if the path is a zip file.
        :param path:  The file to validate
        :raise argparse.ArgumentTypeError: If the file does not end with .zip
        :return:  The path if it is a zip file
        """
        if not path.endswith(".zip"):
            raise argparse.ArgumentTypeError("The file must end with .zip")
        return path

    def unzip(self, file):
        """
        Extract the content of the zip file to the Temp directory.
        :param file: The zip file to extract
        """
        print(f"Unzipping file {file}")
        with zipfile.ZipFile(file, 'r') as zip_ref:
            zip_ref.extractall(self.temp_dir)
        print(f"Extracted to: {self.temp_dir}")

    def copy_zip(self, file):
        """
        Copy the zip file to the Backup directory.
        :param file: The zip file to copy
        """
        print(f"Copying file: {file} to {self.backup_dir}")
        shutil.copy(file, self.backup_dir)
        print(f"Copied to: {self.backup_dir}")

    def process_zip(self):
        """

        Process a zip file passed as a command-line argument. Validates the file extension,
        extracts the content to a temporaty directory and copies the file to a backup directory.

        Logs messages to indicate successful extraction and backup.
        """
        parser = argparse.ArgumentParser(description="Decompress a .zip file.")
        parser.add_argument("file", type=self.zip_file, help=".zip path file")
        args = parser.parse_args()

        # Decompress the file in Temp
        self.unzip(args.file)
        lbox_logger.info(f"File {args.file} has been decompressed.")
        # Copy zip to Backups
        self.copy_zip(args.file)
        lbox_logger.info(f"File {args.file} has been copied to Backups.")
