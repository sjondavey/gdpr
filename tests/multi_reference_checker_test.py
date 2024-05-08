import pytest
from regulations_rag.reference_checker import ReferenceChecker
from gdpr_rag.multi_reference_checker import MultiReferenceChecker

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


class TestMultiReferenceChecker():

    main = MainSection()
    alt = AltSection()
    doc_ref_checker = MultiReferenceChecker([main, alt])

    def test_is_valid(self):
        assert self.doc_ref_checker.is_valid("3.4.2.1")
        assert self.doc_ref_checker.is_valid("Application. Annex 2.1")
        assert not self.doc_ref_checker.is_valid("Application. Annex")

    def test_get_parent_reference(self):
        assert self.doc_ref_checker.get_parent_reference("3.4.2.1") == "3.4.2"
        assert self.doc_ref_checker.get_parent_reference("Application. Part 2") == "Application"