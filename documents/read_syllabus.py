from typing import List
from re import sub


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
