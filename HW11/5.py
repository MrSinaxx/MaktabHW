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


def main():
    parser = argparse.ArgumentParser(description='Calculate the volume (size) of files and folders.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-d', dest='directory', metavar='DIRECTORY', help='calculate the size of a directory')
    group.add_argument('-f', dest='file', metavar='FILE', help='calculate the size of a file')
    parser.add_argument('-F', dest='extension', metavar='EXTENSION', help='filter files by extension')
    
    args = parser.parse_args()
    
    if args.directory:
        size = get_directory_size(args.directory, args.extension)
        print(f"{size} KB")
    elif args.file:
        size = get_file_size(args.file)
        print(f"{size} KB")

if __name__ == '__main__':
    main()