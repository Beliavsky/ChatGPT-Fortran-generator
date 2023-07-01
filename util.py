import os
import shutil
import glob
import shutil

def copy_files(src_dir,dest_dir):
    for root, dirs, files in os.walk(src_dir):
        for f in files:
            shutil.copy(os.path.join(root,f), dest_dir)

def files_in_dir(path,extension):
    os.chdir(path)
    result = [i for i in glob.glob('*.{}'.format(extension))]
    return result

def lines_in_f1_not_f2(f1,f2):
    s1 = open(f1,"r").readlines()
    s2 = open(f2,"r").readlines()
    lines = []
    for word in s2:
        if (word not in s1):
            lines.append(word)
    return lines
    
def truncated_string(original_string, sentinel):
    """ return original string up to the occurrence of sentinel """
    index = original_string.find(sentinel)
    if index != -1:
        truncated_string = original_string[:index]
        return truncated_string
    else:
        return original_string

def save_numbered_file(file_path):
    """
    Copy a file to an unused file name with a numbered suffix.
    Args:
        file_path (str): The path to the file to be copied.
    Returns:
        str: The path of the newly copied file.
    """
    base_dir = os.path.dirname(file_path)
    base_name, ext = os.path.splitext(os.path.basename(file_path))
    new_file_path = file_path
    counter = 1
    while os.path.exists(new_file_path):
        new_file_name = f"{base_name}{counter}{ext}"
        new_file_path = os.path.join(base_dir, new_file_name)
        counter += 1
    shutil.copyfile(file_path, new_file_path)
    return new_file_path
