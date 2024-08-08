import argparse
import datetime
import os

import pandas as pd
from config import DATA_PATH, DATA_URL, HEADERS, DATA_MAP_URL,DATA_MAP_PATH,METHOD
from generation.fetch_data import fetch_data
from generation.fetch_data_map import fetch_data_map
from survey_model.questions import Questions
from generation import fetch_data, fetch_data_map, generate_columns, generate_questions, generate_data_objects, generate_questions_validator
from survey_model import DATA, COLUMNS, QUESTIONS, QUESTIONTYPES, Column, Columns, Question, Questions
from validators import *
from logs import geterrors

def parse_args():
    parser = argparse.ArgumentParser(description="Run type script.")
    parser.add_argument('--type', '-o', help="An optional argument for the script.", default=None)
    return parser.parse_args()

def main():
    args = parse_args()
    runtype="FULLRUN"
    if not os.path.exists(DATA_PATH) or args.type =="GENERATE":
        runtype="GENERATE"
    else:
        current_time = datetime.datetime.now()
        file_mod_time = datetime.datetime.fromtimestamp(os.path.getmtime(DATA_PATH))
        time_diff = current_time - file_mod_time
        if time_diff.total_seconds() <= 3600:
            runtype="VALIDATEONLY"
    if args.type =="FULLRUN":
        runtype="FULLRUN"
    
    if runtype=="GENERATE":
        print("*****GENERATE MODE*****\n")
        flag=True
        if METHOD=="API":
            flag = fetch_data_map(DATA_MAP_URL,HEADERS,DATA_MAP_PATH)
            if flag:
                print("Data Map fetched...")
                flag = fetch_data(DATA_URL,HEADERS,DATA_PATH)
                if flag:
                    print("Data fetched...")
                else:
                    print("Data fetch failed")
            else:
                print("Data Map fetch failed")
        if flag:
            generate_columns(DATA_MAP_PATH,DATA_PATH)
            generate_questions(DATA_MAP_PATH,DATA_PATH)
            generate_questions_validator(DATA_MAP_PATH)
            generate_data_objects(DATA_PATH)

    if runtype=="VALIDATEONLY":
        print(f"*****VALIDATEONLY MODE*****\nRunning validation on existing data downlaoded at {file_mod_time}\n")
        
        print("Starting question validator...")
        question_validator()
        print("Finished question validator...")
        
        print("Starting record validator...")
        record_validator()
        print("Finished record validator...")
        geterrors()

    if runtype=="FULLRUN":
        print(f"*****FULLRUN MODE*****\n")
        flag=True
        if METHOD=="API":
            flag = fetch_data_map(DATA_MAP_URL,HEADERS,DATA_MAP_PATH)
            if flag:
                print("Data Map fetched...")
                flag = fetch_data(DATA_URL,HEADERS,DATA_PATH)
                if flag:
                    print("Data fetched...")
                else:
                    print("Data fetch failed")
            else:
                print("Data Map fetch failed")
        if flag:
            generate_columns(DATA_MAP_PATH,DATA_PATH)
            generate_questions(DATA_MAP_PATH,DATA_PATH)
            generate_data_objects(DATA_PATH)
            
        print("Starting question validator...")
        question_validator()
        print("Finished question validator...")
        
        print("Starting record validator...")
        record_validator()
        print("Finished record validator...")
        geterrors()
 
    

if __name__ == "__main__":
    main()
