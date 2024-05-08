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


class Article_47_BCR(Document):
    def __init__(self, path_to_manual_as_csv_file = "./inputs/documents/article_47_bcr.csv"):

        main = MainSection()
        alt = AltSection()
        analysis = AnalysisSection()
        reference_checker = MultiReferenceChecker([main, alt, analysis])

        path_to_additional_manual_as_csv_file = ""

        self.document_as_df = load_csv_data(path_to_file = path_to_manual_as_csv_file)

        document_name = "Recommendations 1/2022 on the Application for Approval and on the elements and principles to be found in Controller Binding Corporate Rules"
        super().__init__(document_name, reference_checker=reference_checker)
        if not self.check_columns():
            raise AttributeError(f"The input csv file for the Article_47_BCR class does not have the correct column headings")


    def check_columns(self):
        expected_columns = ["section", "point", "section_reference", "heading", "text"] 

        actual_columns = self.document_as_df.columns.to_list()
        for column in expected_columns:
            if column not in actual_columns:
                print(f"{column} not in the DataFrame version of the manual")
                return False
        return True

    def _add_numbering_to_text(self, row, text_extract, heading = False):
        if row["heading"]:
            if row["point"] != "":
                return row["point"] + ". " + text_extract
            else:
                return row["section"] + " " + text_extract
        else:    
            if heading:
                return ""
            if row["point"]:
                return row["point"] + ". " + text_extract
            else:
                return "    " + text_extract

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

                pattern = r'^\d\.\d' # there is a special case here were if I ask for "1.1" for example, the "startswith()" query will also include 1.10, 1.11 etc
                if re.match(pattern, section_reference):
                    tmp1 = self.document_as_df[self.document_as_df["section_reference"].str.startswith(section_reference + ".")] # use startswith to get children as well
                    tmp2 = self.document_as_df[self.document_as_df["section_reference"] == section_reference] 
                    subset = pd.concat([tmp1, tmp2]).sort_index()
                else:
                    subset = self.document_as_df[self.document_as_df["section_reference"].str.startswith(section_reference)] # use startswith to get children as well

            if len(subset) == 0:
                return ""
            for index, row in subset.iterrows():
                footnotes, text_extract = extract_footnotes(row["text"])
                all_footnotes = all_footnotes + footnotes

                text += self._add_numbering_to_text(row, text_extract) + "\n"
            parent = self.reference_checker.get_parent_reference(section_reference)
            build_up = ""
            while parent != "":
                subset = self.document_as_df[self.document_as_df["section_reference"] == parent]
                for index, row in subset[::-1].iterrows(): # backwards
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


class MainSection(ReferenceChecker):
    def __init__(self):
        exclusion_list = [] 
        index_patterns = [
            r'^\d+',   
            r'^\.\d+', 
            r'^\.\d+', 
            r'^\.\d+', 
        ]    
        text_pattern = r'(\d+(\.\d+)?(\.\d+)?(\.\d+)?)'

        super().__init__(regex_list_of_indices = index_patterns, text_version = text_pattern, exclusion_list=exclusion_list)

class AltSection(ReferenceChecker):
    def __init__(self):
        exclusion_list = [] #
        index_patterns = [
            r'\bApplication\b',
            r'\.\s(Part|Annex)\s\d+', # "". Part" or ".Annex"
            r'\.\d+',
        ]
        text_pattern = r'Application. (Part/Annex\s\d+)?(\.(\d+))?'

        super().__init__(regex_list_of_indices = index_patterns, text_version = text_pattern, exclusion_list=exclusion_list)

class AnalysisSection(ReferenceChecker):
    def __init__(self):
        exclusion_list = [] #
        index_patterns = [
            r'\bAnalysis\b',
            r'\s\d+', 
        ]
        text_pattern = r'Analysis (\d+)?'

        super().__init__(regex_list_of_indices = index_patterns, text_version = text_pattern, exclusion_list=exclusion_list)

