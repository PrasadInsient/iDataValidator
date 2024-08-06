from dataclasses import dataclass
from typing import Any, Dict, List
import xml.etree.ElementTree as ET
    
def GetQuestions(jsonObj:Any)->List[Dict[str, str]]:
    questionsMap = []
    for q in jsonObj['variables']:
        if not q['qlabel']:
            questionObj = {}
            questionObj['qtype'] = q['type']
            questionObj['qlabel'] = q['vgroup']
            questionObj['qtitle'] = f"{q['vgroup']} - {q['qtitle']}"
            questionObj['qrows'] = []
            questionObj['qcols'] = []
            questionObj['qdataColumnsNames'] = f"['{q['vgroup']}']"
            questionObj['qOEColumnsNames'] = []
            questionsMap.append(questionObj)

    for q in jsonObj['questions']:
        questionObj = {}
        type = q['type']
        subtype=type
        if type == 'single':
            if 'variables' in q:
                varcnt =0
                for var in q['variables']:
                    if var['type']=="single":
                        varcnt=varcnt+1
                if varcnt > 1:
                    subtype = 'grid'

        if type == 'text':
            if 'variables' in q:
                if len(q['variables']) > 1:
                    subtype = 'textlist'


        if type == 'number':
            if 'variables' in q:
                varcnt =0
                for var in q['variables']:
                    if var['type']=="number":
                        varcnt=varcnt+1
                if varcnt > 1:
                    subtype = 'numberlist'

        if type == 'float':
            type = 'number'
            subtype = 'number'
            if 'variables' in q:
                varcnt =0
                for var in q['variables']:
                    if var['type']=="float":
                        varcnt=varcnt+1
                if varcnt > 1:
                    subtype = 'numberlist'

        questionObj = {}
        questionObj['qtype'] = type
        questionObj['subtype'] = subtype
        questionObj['qlabel'] = q['qlabel']
        questionObj['qtitle'] = q['qtitle']
        rows = []
        cols = []
        dataColumnsNames = []

        if 'variables' in q:
            if subtype == 'single':
                rows = q['values']
                for var in q['variables']:
                    if var['type']=='single':
                        dataColumnsNames.append(var['label'])

            if subtype == 'multiple':
                rows = q['values']
                for var in q['variables']:
                    if var['type']=='multiple':
                        dataColumnsNames.append(var['label'])

            if subtype == 'grid':
                cols = q['values']
                for var in q['variables']:
                    if var['type']=='single':
                        rows.append({'label': var['row'], 'title': var['rowTitle'], 'value': None})
                        dataColumnsNames.append(var['label'])

            if subtype in ['number','float']:
                for var in q['variables']:
                    if var['type']=='number' or var['type']=='float':
                        dataColumnsNames.append(var['label'])

            if subtype in ['numberlist','floatlist']:
                for var in q['variables']:
                    if var['type']=='number' or var['type']=='float':
                        rows.append({'label': var['row'], 'title': var['rowTitle'], 'value': None})
                        dataColumnsNames.append(var['label'])

            if subtype in ['text']:
                for var in q['variables']:
                    dataColumnsNames.append(q['label'])

            if subtype in ['textlist']:
                for var in q['variables']:
                    rows.append({'label': var['row'], 'title': var['rowTitle'], 'value': None})
                    dataColumnsNames.append(var['label'])

        questionObj['qrows'] = rows
        questionObj['qcols'] = cols
        questionObj['qdataColumnsNames'] = dataColumnsNames
        questionObj['qOEColumnsNames'] = ['']
        questionsMap.append(questionObj)
    return questionsMap


def GetColumns(jsonObj:Any)->List[Dict[str, str]]:
    questionsMap = []
    for q in jsonObj['variables']:
        questionObj = {}
        questionObj['type'] = q['type']
        questionObj['label'] = q['label']
        questionsMap.append(questionObj)
    return questionsMap