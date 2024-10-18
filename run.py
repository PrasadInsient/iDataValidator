import argparse
import datetime
import os
import pandas as pd
from config import DATA_PATH, DATA_URL, HEADERS, DATA_MAP_URL, DATA_MAP_PATH, METHOD, PLATFORM
from generate.fetch_data import fetch_data
from generate.fetch_data_map import fetch_data_map
from survey_model.questions import Questions
from generate import * 
from survey_model import DATA, COLUMNS, QUESTIONS, QUESTIONTYPES, Columns, Question, Questions
from validators import *
from logs import geterrors
from tqdm import tqdm

def parse_args():
    parser = argparse.ArgumentParser(description="Run type script.")
    parser.add_argument('-m', '--mode', help="Run mode: GENERATE, VALIDATEONLY, or FULLRUN.", default="VALIDATEONLY")
    return parser.parse_args()

def main():
    args = parse_args()
    runtype = "FULLRUN"
    if not os.path.exists(DATA_PATH) or args.mode == "GENERATE":
        runtype = "GENERATE"
    else:
        current_time = datetime.datetime.now()
        file_mod_time = datetime.datetime.fromtimestamp(os.path.getmtime(DATA_PATH))
        time_diff = current_time - file_mod_time

        if time_diff.total_seconds() <= 3600:
            runtype = "VALIDATEONLY"
        if args.mode == "FULLRUN":
            runtype = "FULLRUN"
    
    if runtype == "GENERATE":
        print("***** GENERATE MODE *****\n")
        run_generate()

    elif runtype == "VALIDATEONLY":
        print(f"***** VALIDATEONLY MODE *****\nRunning validation on existing data downloaded at {file_mod_time}.\n")
        run_validation()

    elif runtype == "FULLRUN":
        print("***** FULLRUN MODE *****\n")
        run_full()

def run_generate():
    flag = True
    if METHOD == "API":
        flag = fetch_data_map(DATA_MAP_URL, HEADERS, DATA_MAP_PATH)
        if flag:
            print("Data Map fetched...")
            flag = fetch_data(DATA_URL, HEADERS, DATA_PATH)
            if flag:
                print("Data fetched...")
            else:
                print("Data fetch failed")
        else:
            print("Data Map fetch failed")
    
    if flag:
        generate_columns(DATA_MAP_PATH, DATA_PATH)
        generate_questions(DATA_MAP_PATH, DATA_PATH)
        generate_datarecord(DATA_MAP_PATH, DATA_PATH)
        generate_validators(DATA_MAP_PATH)
        generate_data_objects(DATA_PATH)

def run_validation():
    tot_records = len(DATA)
    records_completed = 0
    print(f"Starting validator on {tot_records} records")
    tqdm.pandas(desc="Validating Records")
    def runv(row):
        nonlocal records_completed  # This allows modification of the outer scope variable
        row_fill=row.fillna(False)
        validator(row_fill)
        validatorx1(row_fill)
        validatorx2(row_fill)
        records_completed += 1
        return row

    # Apply the validation function to each row in DATA
    DATA.apply(runv, axis=1)
    
    print(f"Finished validator : {records_completed} out of {tot_records}")
    geterrors()


def run_full():
    flag = True
    if METHOD == "API":
        flag = fetch_data_map(DATA_MAP_URL, HEADERS, DATA_MAP_PATH)
        if flag:
            print("Data Map fetched...")
            flag = fetch_data(DATA_URL, HEADERS, DATA_PATH)
            if flag:
                print("Data fetched...")
            else:
                print("Data fetch failed")
        else:
            print("Data Map fetch failed")

    if flag:
        generate_columns(DATA_MAP_PATH, DATA_PATH)
        generate_questions(DATA_MAP_PATH, DATA_PATH)
        generate_data_objects(DATA_PATH)
        
    run_validation()

    geterrors()

if __name__ == "__main__":
    main()
