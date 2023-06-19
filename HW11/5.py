import os
import argparse

def get_file_size(file_path):
    return os.path.getsize(file_path) // 1024