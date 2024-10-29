import argparse
import shutil
import zipfile


def zip_file(path):
    if not path.endswith(".zip"):
        raise argparse.ArgumentTypeError("The file must end with  .zip")
    return path

def unzip(file):
    with zipfile.ZipFile(file, 'r') as zip_ref:
        zip_ref.extractall('FilmioData/Temp')

def copy_zip(file):
    shutil.copy(file, 'FilmioData/Backup')