import os
import ast
import inspect

def extract_functions_from_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        node = ast.parse(file.read(), filename=file_path)
    
    functions = [n for n in node.body if isinstance(n, ast.FunctionDef)]
    print(f"\nModule: {file_path}")
    for function in functions:
        print(f"Function: {function.name}")
        args = [arg.arg for arg in function.args.args]
        print(f"Signature: ({', '.join(args)})")
        docstring = ast.get_docstring(function)
        if docstring:
            print(f"Docstring:\n{docstring}")
        else:
            print("Docstring: None")
        print("")

def print_function_docs_in_directory(directory, exclude_dirs=None, exclude_files=None):
    if exclude_dirs is None:
        exclude_dirs = ['.git', '__pycache__']
    if exclude_files is None:
        exclude_files = ['*.pyc']

    for root, _, files in os.walk(directory):
        if any(excluded in root for excluded in exclude_dirs):
            continue
        for file in files:
            if file.endswith(".py") and not any(file.endswith(ext) for ext in exclude_files):
                file_path = os.path.join(root, file)
                extract_functions_from_file(file_path)

# Example usage:
print_function_docs_in_directory('/Users/prasad/github/iDataValidator/validator_functions')
