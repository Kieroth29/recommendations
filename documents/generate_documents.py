from csv import writer
from typing import Dict, List


def export_sheet(recommendations: List[Dict]) -> None:
    with open("recommendations.csv", "w") as file:
        file_writer = writer(file)
        file_writer.writerow(["Title", "Authors", "Year", "Venue", "URL"])

        for recommendation in recommendations:
            file_writer.writerow(recommendation)
