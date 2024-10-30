import argparse
import shutil
import zipfile

from FilmioBack.logger_config import lbox_logger


class ZipHandler:
    def __init__(self, temp_dir='Data/Temp', backup_dir='Data/Backup'):
        self.temp_dir = temp_dir
        self.backup_dir = backup_dir

    def zip_file(self, path):
        if not path.endswith(".zip"):
            raise argparse.ArgumentTypeError("The file must end with .zip")
        return path

    def unzip(self, file):
        print(f"Unzipping file {file}")
        with zipfile.ZipFile(file, 'r') as zip_ref:
            zip_ref.extractall(self.temp_dir)
        print(f"Extracted to: {self.temp_dir}")

    def copy_zip(self, file):
        print(f"Copying file: {file} to {self.backup_dir}")
        shutil.copy(file, self.backup_dir)
        print(f"Copied to: {self.backup_dir}")


    def process_zip(self):
        parser = argparse.ArgumentParser(description="Decompress a .zip file.")
        parser.add_argument("file", type=self.zip_file, help=".zip path file")
        args = parser.parse_args()

        # Decompress the file in Temp
        self.unzip(args.file)
        lbox_logger.info(f"File {args.file} has been decompressed.")
        # Copy zip to Backups
        self.copy_zip(args.file)
        lbox_logger.info(f"File {args.file} has been copied to Backups.")
