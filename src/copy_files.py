import os
import shutil


def copy_files(from_path, to_path):
    if not os.path.isdir(from_path):
        raise Exception("Path from you want to copy from doesn't exists")
    shutil.rmtree(to_path, ignore_errors=True)

    if not os.path.exists(os.path.abspath(to_path)):
        os.mkdir(os.path.abspath(to_path))
    files = os.listdir(from_path)
    for file in files:
        if os.path.isdir(os.path.join(os.path.abspath(from_path), file)):
            copy_files(os.path.join(from_path, file), os.path.join(to_path, file))
            continue
        shutil.copy(os.path.join(from_path, file), os.path.join(to_path, file))
