import re
from regulations_rag.reference_checker import ReferenceChecker

class MultiReferenceChecker(ReferenceChecker):
    def __init__(self, list_of_reference_checkers):
        self.list_of_reference_checkers = list_of_reference_checkers

    def is_valid(self, reference):
        for ref_checker in self.list_of_reference_checkers:
            if ref_checker.is_valid(reference):
                return True
        return False

    def extract_valid_reference(self, reference):
        raise NotImplementedError()

    def split_reference(self, reference):
        for ref_checker in self.list_of_reference_checkers:
            if ref_checker.is_valid(reference):
                return ref_checker.split_reference(reference)
        return ""

    def get_parent_reference(self, reference):
        for ref_checker in self.list_of_reference_checkers:
            if ref_checker.is_valid(reference):
                return ref_checker.get_parent_reference(reference)
        return ""
    
    def get_current_and_parent_references(self, reference):
        raise NotImplementedError()

    def is_reference_or_parents_in_list(self, reference, list_of_references):
        raise NotImplementedError()

    def _extract_reference_from_string(self, s):
        raise NotImplementedError()



