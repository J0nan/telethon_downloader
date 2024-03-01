import os
import shutil

import logger
from constants import EnvironmentReader


class Utils:
    def __init__(self, constants=[]):
        self.constants = EnvironmentReader()
        self.PERMISSIONS_FOLDER = int(self.constants.PERMISSIONS_FOLDER)
        self.PERMISSIONS_FILE = int(self.constants.PERMISSIONS_FILE)
        self.permisos_octal_folder = int(str(self.PERMISSIONS_FOLDER), 8)
        self.permisos_octal_file = int(str(self.PERMISSIONS_FILE), 8)
        self.PUID = (
            int(self.constants.PUID) if (str(self.constants.PUID)).isdigit() else None
        )
        self.PGID = (
            int(self.constants.PGID) if (str(self.constants.PGID)).isdigit() else None
        )

    def rename_file(self, old_path, new_path):
        try:
            logger.logger.info(f"rename_file => {old_path}, {new_path}")

            self.create_folders(new_path)
            shutil.move(old_path, new_path)
            self.change_owner_permissions(new_path)
            return True
        except Exception as e:
            logger.logger.info(f"rename_file => Exception {e}")
            return False

    def change_permissions(self, file_name):
        try:
            if os.path.isfile(file_name):
                os.chmod(file_name, self.permisos_octal_file)
                print(
                    f"Permissions of the file {file_name} changed to {self.PERMISSIONS_FILE}"
                )
            elif os.path.isdir(file_name):
                os.chmod(file_name, self.permisos_octal_folder)
                print(
                    f"Permissions of the file {file_name} changed to {self.PERMISSIONS_FOLDER}"
                )
            else:
                print(f"{file_name} does not exist or is not a file or directory.")

        except FileNotFoundError:
            print(f"The file {file_name} was not found")

    def change_owner(self, file_name):
        try:
            if self.PUID and self.PGID:
                os.chown(file_name, self.PUID, self.PGID)
                print(
                    f"Owner of the file {file_name} changed to {self.PUID} {self.PGID}"
                )
        except FileNotFoundError:
            print(f"The file {file_name} was not found")

    def create_folder(self, folder_name):
        try:
            os.makedirs(folder_name, exist_ok=True)
            self.change_owner_permissions(folder_name)
            print(f"Folder {folder_name} created")
        except FileExistsError:
            print(f"The folder {folder_name} already exists")

    def create_folders(self, folder_name):
        try:
            # Verificar si la folder_name es un archivo
            if os.path.isfile(folder_name):
                base_directory = os.path.dirname(folder_name)
                self.create_folder(base_directory)
            elif os.path.isdir(folder_name):
                self.create_folder(folder_name)
            else:
                base_directory = os.path.dirname(folder_name)
                self.create_folder(base_directory)
                logger.logger.info(
                    f"{folder_name} does not exist or is not a file or directory."
                )

            if self.PUID and self.PGID:
                self.change_owner(folder_name)

            self.change_permissions(folder_name)
        except FileExistsError:
            print(f"The folder {folder_name} already exists")

    def change_owner_permissions(self, folder_name):
        try:
            if self.PUID and self.PGID:
                self.change_owner(folder_name)
            self.change_permissions(folder_name)
        except Exception as e:
            print(f"change_owner_permissions Exception: {folder_name}: {e}")


# Example of usage
if __name__ == "__main__":
    folder_creator = Utils()
    folder_creator.create_folders("/audios/youtube/A/B/C/D")
    folder_creator.create_folders("/audios/youtube/A/B/C/D/lala.txt")
