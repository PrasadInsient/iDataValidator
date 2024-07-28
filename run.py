import argparse

import pandas as pd
from config import DATA_PATH, DATA_URL, HEADERS, DATA_MAP_URL,DATA_MAP_PATH
from generation.fetch_data import fetch_data
from generation.fetch_data_map import fetch_data_map
from survey_model.questions import Questions
from generation import fetch_data, fetch_data_map, generate_columns, generate_questions, generate_data_objects, generate_questions_validator
from survey_model import DATA, COLUMNS, QUESTIONS, QUESTIONTYPES, Column, Columns, Question, Questions
from validators import *
from logs import geterrors

def parse_args():
    parser = argparse.ArgumentParser(description="Script to check if the first argument is 'gen'.")
    parser.add_argument("command", help="The command to process, should be 'gen'.")
    return parser.parse_args()

def main():
    args = parse_args()
    if args.command == "gen":
        print("Starting the file generation process")
        fetch_data_map(DATA_MAP_URL,HEADERS,DATA_MAP_PATH)
        fetch_data(DATA_URL,HEADERS,DATA_PATH)
        generate_columns(DATA_MAP_PATH,DATA_PATH)
        generate_questions(DATA_MAP_PATH,DATA_PATH)
        generate_questions_validator(DATA_MAP_PATH)
        generate_data_objects(DATA_PATH)
    elif args.command == "all":
        print("Running validation by generation and downloading all files...")
        fetch_data_map(DATA_MAP_URL,HEADERS,DATA_MAP_PATH)
        fetch_data(DATA_URL,HEADERS,DATA_PATH)
        generate_columns(DATA_MAP_PATH,DATA_PATH)
        generate_questions(DATA_MAP_PATH,DATA_PATH)
        generate_data_objects(DATA_PATH)

        print("Starting question validator...")
        question_validator()
        print("Finished question validator...")
        
        print("Starting unit validator...")
        unit_validator()
        print("Finished unit validator...")
        
        print("Starting record validator...")
        record_validator()
        print("Finished record validator...")
    else:
        print("Running validation on exisiintg data and existing files...")
        
        print("Starting question validator...")
        question_validator()
        print("Finished question validator...")
        
        print("Starting unit validator...")
        unit_validator()
        print("Finished unit validator...")
        
        print("Starting record validator...")
        record_validator()
        print("Finished record validator...")
    
    geterrors()

if __name__ == "__main__":
    main()
