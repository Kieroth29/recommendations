from csv import writer
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


def extract_classes_subjects(classes: List[str]) -> None:
    pattern = "Aula[0-9]{2}: "
    for item in classes:
        subject = sub(pattern, '', item)
        
        classes[classes.index(item)] = subject
        

def get_recommendations(content_list: List[str]) -> List[List[str | List[str]]]:
    recommendations = []
    
    for content in content_list:
        pubs = scholarly.search_pubs(content)
        top_pub = next(pubs)
        
        recommendations.append([
            top_pub["bib"]["title"],
            ', '.join(top_pub["bib"]["author"]),
            top_pub["bib"]["pub_year"],
            top_pub["bib"]["venue"],
            top_pub["pub_url"]
        ])
    
    return recommendations


def export_sheet(recommendations: List[Dict]) -> None:
    with open("recommendations.csv", "w") as file:
        file_writer = writer(file)
        file_writer.writerow(["Title", "Authors", "Year", "Venue", "URL"])
        
        for recommendation in recommendations:
            file_writer.writerow(recommendation)
              

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
    
    recommendations = get_recommendations(programatic_content)
    export_sheet(recommendations)
