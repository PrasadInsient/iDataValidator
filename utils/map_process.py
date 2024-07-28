from dataclasses import dataclass
import xml.etree.ElementTree as ET
    
def GetQuestions(jsonObj):
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
        
        if type == 'single':
            type="multiple"

        if type == 'single':
            if 'variables' in q:
                varcnt =0
                for var in q['variables']:
                    if var['type']=="single":
                        varcnt=varcnt+1
                if varcnt > 1:
                    type = 'singlegrid'

        if type == 'text':
            if 'variables' in q:
                #print (q['qlabel'],q['variables'])
                if len(q['variables']) > 1:
                    type = 'textlist'

        if type == 'number':
            if 'variables' in q:
                varcnt =0
                for var in q['variables']:
                    if var['type']=="number":
                        varcnt=varcnt+1
                if varcnt > 1:
                    type = 'numericlist'

        if type == 'float':
            type = 'number'
            if 'variables' in q:
                varcnt =0
                for var in q['variables']:
                    if var['type']=="float":
                        varcnt=varcnt+1
                if varcnt > 1:
                    type = 'numericlist'

        questionObj = {}
        questionObj['qtype'] = type
        questionObj['qlabel'] = q['qlabel']
        questionObj['qtitle'] = q['qtitle']
        rows = []
        cols = []
        dataColumnsNames = []

        if 'variables' in q:
            if type == 'single':
                rows = q['values']
                dataColumnsNames.append(q['qlabel'])

            if type == 'singlegrid':
                cols = q['values']
                for var in q['variables']:
                    rows.append({'label': var['row'], 'title': var['rowTitle'], 'value': None})
                    dataColumnsNames.append(var['label'])

            if type in ['text','number','float']:
                dataColumnsNames.append(q['qlabel'])

            if type in ['textlist','numberlist','floatlist']:
                dataColumnsNames.append(q['qlabel'])
                for var in q['variables']:
                    rows.append({'label': var['row'], 'title': var['rowTitle'], 'value': None})
                    dataColumnsNames.append(var['label'])

        questionObj['qrows'] = rows
        questionObj['qcols'] = cols
        questionObj['qdataColumnsNames'] = dataColumnsNames
        questionObj['qOEColumnsNames'] = ['']
        questionsMap.append(questionObj)
    return questionsMap


def GetColumns(jsonObj):
    questionsMap = []
    for q in jsonObj['variables']:
        questionObj = {}
        questionObj['type'] = q['type']
        questionObj['label'] = q['label']
        questionsMap.append(questionObj)
    return questionsMap