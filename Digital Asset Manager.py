import os
import shutil
from pathlib import Path

def organize_files(directory):
    path = Path(directory)
    for file in path.iterdir():
        if file.is_file():
            ext = file.suffix.lower()[1:]
            dest = path / ext
            dest.mkdir(exist_ok=True)
            shutil.move(str(file), str(dest / file.name))
    print(f"Files in {directory} organized!")

# Example usage:
organize_files('/Users/You/Downloads')