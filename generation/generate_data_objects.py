def generate_data_objects(DATA_PATH):
    data_file = 'survey_model/data_objects.py'
    
    with open(data_file, 'w') as f:
        f.write("import pandas as pd\n")
        f.write("from .columns import Columns\n")
        f.write("from .questions import Questions\n")
        f.write("from .questiontypes import QuestionTypes\n")
        try:
            f.write(f"DATA= pd.read_excel('{DATA_PATH}')\n")
            f.write(f"COLUMNS = Columns()\n")
            f.write(f"QUESTIONS = Questions()\n")
            f.write(f"QUESTIONTYPES = QuestionTypes()\n")
            print(f"Data Objects file '{data_file}' generated successfully.")
        except:
            print("Error in DATA Objects Generation")
    