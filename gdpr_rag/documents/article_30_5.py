import pandas as pd
from regulations_rag.regulation_reader import  load_regulation_data_from_files
from gdpr_rag.document import Document
from gdpr_rag.empty_reference_checker import EmptyReferenceChecker


class Article_30_5(Document):
    def __init__(self):
        reference_checker = EmptyReferenceChecker()

        path_to_manual_as_csv_file = "./inputs/documents/article_30_5.csv"
        path_to_additional_manual_as_csv_file = ""

        document_as_df = load_regulation_data_from_files(path_to_manual_as_csv_file = path_to_manual_as_csv_file, 
                                                         path_to_additional_manual_as_csv_file = path_to_additional_manual_as_csv_file)

        document_name = "WORKING PARTY 29 POSITION PAPER on the derogations from the obligation to maintain records of processing activities pursuant to Article 30(5) GDPR"
        super().__init__(document_name, document_as_df = document_as_df, reference_checker=reference_checker)

    def check_columns(self):
        expected_columns = ["section_reference", "heading", "text"] 

        actual_columns = self.document_as_df.columns.to_list()
        for column in expected_columns:
            if column not in actual_columns:
                print(f"{column} not in the DataFrame version of the manual")
                return False
        return True


    def get_text(self, section_reference):        
        return self.document_as_df.iloc[0]['text']


    def get_heading(self, section_reference):
        return "Entire document"
