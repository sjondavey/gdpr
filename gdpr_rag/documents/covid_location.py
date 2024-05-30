import re
import pandas as pd
from regulations_rag.regulation_reader import  load_csv_data
from regulations_rag.document import Document
from regulations_rag.reference_checker import ReferenceChecker
from regulations_rag.reference_checker import MultiReferenceChecker



class CovidLocation(Document):
    def __init__(self, path_to_manual_as_csv_file = "./inputs/documents/covid_location.parquet"):

        reference_checker =  self.CovidLocationReferenceChecker()


        #self.document_as_df = load_csv_data(path_to_file = path_to_manual_as_csv_file)
        self.document_as_df = pd.read_parquet(path_to_manual_as_csv_file, engine = 'pyarrow')

        document_name = "Guidelines 04/2020 on the use of location data and contact tracing tools in the context of the COVID-19 outbreak"
        super().__init__(document_name, reference_checker=reference_checker)
        if not self.check_columns():
            raise AttributeError(f"The input parquet file for the CovidLocation class does not have the correct column headings")


    def check_columns(self):
        expected_columns = ["section", "subsection", "point", "heading", "text", "section_reference"]

        actual_columns = self.document_as_df.columns.to_list()
        for column in expected_columns:
            if column not in actual_columns:
                print(f"{column} not in the DataFrame version of the DecisionMaking csv file")
                return False
        return True

    def _add_numbering_to_text(self, row, text_extract, heading = False):
        if row["heading"]:
            return row["section_reference"] + " " + text_extract
        else:    
            if heading:
                return ""
            return text_extract

    def get_text(self, section_reference, add_markdown_decorators = True, footnote_pattern = r'^\[\^\d+\]\:'):               
        return super().get_text_for_section_only(section_reference, add_markdown_decorators, footnote_pattern)


    def get_heading(self, section_reference, add_markdown_decorators = False, footnote_pattern = r'^\[\^\d+\]\:'):
        return super().get_heading(section_reference, add_markdown_decorators, footnote_pattern)


    class CovidLocationReferenceChecker(ReferenceChecker):
        def __init__(self):
            exclusion_list = ["Annex"] 
            index_patterns = [
                r'^(\d+)', 
                r'^\.(\d+)', 
            ]    
            text_pattern = r'(\d+)(\.(\d+))?'

            super().__init__(regex_list_of_indices = index_patterns, text_version = text_pattern, exclusion_list=exclusion_list)

