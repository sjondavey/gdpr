import pandas as pd
from gdpr_rag.empty_reference_checker import EmptyReferenceChecker

class TestEmptyReferenceChecker():
    no_reference = EmptyReferenceChecker()

    def test_construction(self):
        assert True

    def test_is_valid(self):
        assert self.no_reference.is_valid("")
        assert not self.no_reference.is_valid("A")
        assert self.no_reference.is_valid(None)

        data = ["", "article_30_5"]
        df = pd.DataFrame([data], columns=["section_reference", "document"])
        empty_df_entry = df.iloc[0]["section_reference"]
        assert self.no_reference.is_valid(empty_df_entry)

        data = [None, "article_30_5"]
        df = pd.DataFrame([data], columns=["section_reference", "document"])
        empty_df_entry = df.iloc[0]["section_reference"]
        assert self.no_reference.is_valid(empty_df_entry)
    # def extract_valid_reference(self, input_string):
    #     return ""
    
    # def split_reference(self, reference):
    #     return ""

    # def get_parent_reference(self, input_string):
    #     return ""

    # def get_current_and_parent_references(self, reference):
    #     return [""]

    # def is_reference_or_parents_in_list(self, reference, list_of_references):
    #     super().is_reference_or_parents_in_list(reference, list_of_references) 

    # def _extract_reference_from_string(self, s):
    #     return ""
