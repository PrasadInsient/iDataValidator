from dataclasses import dataclass
import xml.etree.ElementTree as ET

@dataclass 
class SurveyElements:
    name:str    = ""
    link:str = "" 
    quesitons=None
    
def parse_survey_xml(xml_string):
    s = SurveyElements()
    print(xml_string)
    root = ET.fromstring(xml_string)
    print(root)
    questions = []
    for q in root.findall('question'):
        qid = q.attrib['id']
        qtype = q.attrib['type']
        text = q.find('text').text #type:ignore
        choices = [choice.text for choice in q.findall('choice')] if qtype == 'multiple-choice' else []
        questions.append({'id': qid, 'type': qtype, 'text': text, 'choices': choices})
    return questions
