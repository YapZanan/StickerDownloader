import os
import zipfile


def zip_folder(folder_name):
    with zipfile.ZipFile(f'cache/{folder_name}.zip', 'w') as zipf:
        for root, dirs, files in os.walk(f'cache/{folder_name}'):
            for file in files:
                zipf.write(os.path.join(root, file), arcname=file)