import base64
import glob
import fileinput
import os
import re
import sys
import zlib
from shutil import copymode, move
from posix import remove
from tempfile import mkstemp

def convert(path):
    try:
        with open(path, 'rb') as puml:
            return f'![](https://kroki.io/plantuml/svg/{base64.urlsafe_b64encode(zlib.compress(puml.read(), 9)).decode("utf-8")})'
    except FileNotFoundError:
        print("file {} does not exist".format(path))

def replace(match_obj):
    if match_obj.group() is not None:
        path = match_obj.group()[len('~puml:'):-len('~')]
        return convert(path)

def main():
    files = glob.glob1("", '*.md')
    for f in files:
        print(f'Processing: {f}')
        file_path = os.path.basename(f)
        fh, abs_path = mkstemp()
        with os.fdopen(fh,'w') as new_file:
            with open(file_path, 'r') as fin:
                datafile = fin.readlines()
                for line in datafile:
                    new_file.write(re.sub(r'~puml:.*~', replace, line))
        #Copy the file permissions from the old file to the new file
        copymode(file_path, abs_path)
        #Remove original file
        remove(file_path)
        #Move new file
        move(abs_path, file_path)

if __name__ == "__main__":
    main()
