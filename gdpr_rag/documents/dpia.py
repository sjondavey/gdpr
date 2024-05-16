import re
import pandas as pd
from regulations_rag.regulation_reader import  load_csv_data
from regulations_rag.document import Document
from regulations_rag.reference_checker import ReferenceChecker

from regulations_rag.reference_checker import MultiReferenceChecker

def extract_footnotes(text):
    lines = text.split('\n')
    footnotes = []
    remaining_text = []

    for line in lines:
        if re.match(r'^\[\^\d+\]', line):
            footnotes.append(line)
        else:
            remaining_text.append(line)

    text = '\n'.join(remaining_text)
    return footnotes, text


class DPIA(Document):
    def __init__(self, path_to_manual_as_csv_file = "./inputs/documents/dpia.parquet"):

        main =  self.DecisionMakingReferenceChecker()
        annex = self.AnnexSectionReferenceChecker()
        reference_checker = MultiReferenceChecker([main, annex])

        #self.document_as_df = load_csv_data(path_to_file = path_to_manual_as_csv_file)
        self.document_as_df = pd.read_parquet(path_to_manual_as_csv_file, engine = 'pyarrow')

        document_name = "Guidelines on Data Protection Impact Assessment (DPIA) and determining whether processing is 'likely to result in a high risk' for the purposes of Regulation 2016/679"
        super().__init__(document_name, reference_checker=reference_checker)
        if not self.check_columns():
            raise AttributeError(f"The input csv file for the DecisionMaking class does not have the correct column headings")


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
            if row["point"] != "":
                return row["point"] + ". " + text_extract
            elif row["subsection"] != "":
                return row["subsection"] + ". " + text_extract
            else:
                return row["section"] + ". " + text_extract
        else:    
            if heading:
                return ""
            if row["point"]:
                return " " * 8 + text_extract
            elif row["subsection"]:
                return " " * 4 +  text_extract
            else:
                return text_extract

    def get_text(self, section_reference):               
        if not (section_reference == "" or self.reference_checker.is_valid(section_reference)):
            return "" 
        else:
            footnote_pattern = r'\[\^\d+\]'

            text = ""
            all_footnotes = []
            if section_reference == "":
                subset = self.document_as_df
            else:
                subset = self.document_as_df[self.document_as_df["section_reference"] == section_reference] 

            if len(subset) == 0:
                return ""
            for index, row in subset.iterrows():
                if row['text'].startswith("|"): # not table 
                    pass
                elif row['text'].strip() == "The following examples illustrate how the criteria should be used to assess whether a particular processing operation requires a DPIA:":
                    pass
                else: # process  
                    footnotes, text_extract = extract_footnotes(row["text"])
                    all_footnotes = all_footnotes + footnotes
                    text += self._add_numbering_to_text(row, text_extract) + "\n"
            parent = self.reference_checker.get_parent_reference(section_reference)
            build_up = ""
            while parent != "":

                subset = self.document_as_df[self.document_as_df["section_reference"] == parent]
                for index, row in subset[::-1].iterrows(): # backwards
                    if row["heading"]:
                        footnotes, text_extract = extract_footnotes(row["text"])
                        all_footnotes = all_footnotes + footnotes
                        build_up = self._add_numbering_to_text(row, text_extract) + "\n" + build_up


                parent = self.reference_checker.get_parent_reference(parent)
            if build_up != "":
                text = build_up + "\n" + text
            for footnote in all_footnotes:
                text = text + "\n" + footnote

            return text.strip()


    def get_heading(self, section_reference):
        if not self.reference_checker.is_valid(section_reference):
            return "" 
        else:
            footnote_pattern = r'\[\^\d+\]'

            text = ""
            all_footnotes = []
            subset = self.document_as_df[self.document_as_df["section_reference"] == (section_reference)]
            if len(subset) > 0:
                for index, row in subset.iterrows():
                    footnotes, text_extract = extract_footnotes(row["text"])
                    formatted_text = self._add_numbering_to_text(row, text_extract, True)
                    if formatted_text:
                        all_footnotes = all_footnotes + footnotes
                        if text == "":
                            text = formatted_text
                        else:
                            text += "\n" + formatted_text

                parent = self.reference_checker.get_parent_reference(section_reference)
                build_up = ""
                while parent != "":
                    subset = self.document_as_df[self.document_as_df["section_reference"] == parent]
                    for index, row in subset[::-1].iterrows(): # backwards
                        footnotes, text_extract = extract_footnotes(row["text"])
                        formatted_text = self._add_numbering_to_text(row, text_extract, True)
                        if formatted_text:
                            all_footnotes = all_footnotes + footnotes
                            if build_up == "":
                                build_up = formatted_text    
                            else:
                                build_up = formatted_text + "\n" + build_up

                    parent = self.reference_checker.get_parent_reference(parent)
                text = build_up + "\n" + text
                for footnote in all_footnotes:
                    text = text + "\n" + footnote

            return text.strip()


    class DecisionMakingReferenceChecker(ReferenceChecker):
        def __init__(self):
            exclusion_list = [] 
            index_patterns = [
                r'^\b(I|II|III|IV|V|VI)\b',   
                r'^\.([A-Z])', 
                r'^\.([a-z])', 
            ]    
            text_pattern = r'(I|II|III|IV|V|VI)(\.([A-Z]))?(\.([a-z])))?'

            super().__init__(regex_list_of_indices = index_patterns, text_version = text_pattern, exclusion_list=exclusion_list)

    class AnnexSectionReferenceChecker(ReferenceChecker):
        def __init__(self):
            exclusion_list = [] #
            index_patterns = [
                r'^Annex (\d+)'
            ]
            text_pattern = r'Annex \d+'

            super().__init__(regex_list_of_indices = index_patterns, text_version = text_pattern, exclusion_list=exclusion_list)
