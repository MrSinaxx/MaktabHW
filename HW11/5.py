import os
import argparse

def get_file_size(file_path):
    return os.path.getsize(file_path) // 1024

def get_directory_size(directory_path, extension=None):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(directory_path):
        for filename in filenames:
            if extension is None or filename.endswith(extension):
                file_path = os.path.join(dirpath, filename)
                total_size += get_file_size(file_path)
    return total_size