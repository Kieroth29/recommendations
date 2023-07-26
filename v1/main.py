from PyPDF2 import PdfReader
from re import sub
from scholarly import scholarly
from typing import Dict, List


def get_programatic_content(page_text: str) -> List[str]:
    classes = []
    
    lines = page_text.strip().replace("\n ", "").split('\n')

    programatic_content = False

    for line in lines:
        if lines.index(line) > 0:
            previous_line = lines.index(line) - 1
        next_line = lines.index(line) + 1
        
        if 'previous_line' in locals():
            if lines[previous_line] == "CONTEÚDO PROGRAMÁTICO " or lines[previous_line] == "CONTEÚDO PROGRAMÁTICO":
                programatic_content = True
        
        if programatic_content:
            classes.append(line)

        if lines[next_line] == "METODOLOGIA DE ENSINO-APRENDIZAGEM" or lines[next_line] == "METODOLOGIA DE ENSINO-APRENDIZAGEM ":
            break
        
    return classes


def extract_classes_subjects(classes: List[str]):
    pattern = "Aula[0-9]{2}: "
    for item in classes:
        subject = sub(pattern, '', item)
        
        classes[classes.index(item)] = subject
        

def get_recommendations(subject: str) -> Dict:
    pubs = scholarly.search_pubs(subject)
    #TODO: Filter pubs per 'gsrank' key and create top 10 recommendations
        

with open('../resources/MATC84-LaboratorioProgramacaoWeb_(2021.2).pdf', 'rb') as pdfFile:
    pdfReader = PdfReader(pdfFile)
    
    programatic_content = []

    for page_number in range(0, len(pdfReader.pages)):
        page = pdfReader.pages[page_number]
        page_text = page.extract_text()
        
        if "CONTEÚDO PROGRAMÁTICO" in page_text:
            programatic_content = get_programatic_content(page_text)
            break
    
    extract_classes_subjects(programatic_content)
    for subject in programatic_content:
        get_recommendations(subject)
