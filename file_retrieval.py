import os
import filecmp
import shutil
import zipfile
import tarfile
import tempfile
import hashlib
import logging
import sys
import subprocess
import platform

import hash_manager
import cryptography

logger = logging.getLogger(__name__)



def get_file_type(file):
    split = file.split('.')
    ending = split[-1] if len(split) == 2 else split[1:].join(".")
    ending = "." + ending
    return ending

class FileReader:
    def __init__(self, id=None, file_path=None, file_name=None, file_hash=None, file_size=None, file_url=None, file_type=None):
        self.file_type = file_type
        self.file_path = file_path
        self.file_name = file_name
        self.file_hash = file_hash
        self.file_size = file_size
        self.file_url = file_url
        self.id = id

        self.is_encrypted = None
        self.hasher = hash_manager.HashManager()

    def get_file_info(self):
        return {
                "file type" : self.file_type,
                "file path" : self.file_path,
                "file name" : self.file_name,
                "file hash" : self.file_hash,
                "file size" : self.file_size,
                "file url" : self.file_url
                }

    def add_file(self, filename, directory=None, url=None):
        logger.info("Adding file: " + filename)

        self.file_url = url
        if directory is None:
            directory = os.getcwd()
        if not os.path.exists(os.path.join(directory, filename)):
            self.file_path = os.path.join(directory, filename)
        else:
            try:
                print("File already exists, would you like to overwrite it? (y/n): ")
                answer = input()
                if answer.lower() == "y":
                    shutil.copyfile(os.path.join(directory, filename), self.file_path)
                else:
                    self.file_name = self.file_name + str(self.id)
            except:
                print("Error: File already exists and could not be overwritten.")

        self.file_name = os.path.basename(filename)
        self.file_type = get_file_type(filename)
        self.file_hash = self.hasher.calculate_sha256(self.file_path)
        self.file_size = os.path.getsize(self.file_path)


