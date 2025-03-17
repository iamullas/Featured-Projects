import os

folder_path = "path/to/your/folder"
prefix = "new_name_"

for index, filename in enumerate(os.listdir(folder_path)):
    if filename.endswith(".txt"):  # Change this for different file types
        new_name = f"{prefix}{index}.txt"
        old_path = os.path.join(folder_path, filename)
        new_path = os.path.join(folder_path, new_name)
        os.rename(old_path, new_path)

print("Files renamed successfully!")
