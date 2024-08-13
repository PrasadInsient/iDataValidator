import os

def print_directory_structure(directory, prefix='', exclude_dirs=None, exclude_files=None):
    if exclude_dirs is None:
        exclude_dirs = ['.git', '__pycache__']
    if exclude_files is None:
        exclude_files = ['*.pyc']

    items = [item for item in os.listdir(directory) if item not in exclude_dirs and not any(item.endswith(ext) for ext in exclude_files)]
    
    print(prefix + os.path.basename(directory) + "/")
    prefix += "│   "
    
    for index, item in enumerate(items):
        path = os.path.join(directory, item)
        if index == len(items) - 1:
            connector = "└── "
            new_prefix = prefix.replace("│   ", "    ", 1)
        else:
            connector = "├── "
            new_prefix = prefix

        if os.path.isdir(path):
            print(new_prefix[:-4] + connector + item + "/")
            print_directory_structure(path, new_prefix, exclude_dirs, exclude_files)
        else:
            print(new_prefix[:-4] + connector + item)

# Example usage:
print_directory_structure('/Users/prasad/github/iDataValidator')
