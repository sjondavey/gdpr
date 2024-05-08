from regulations_rag.reference_checker import ReferenceChecker


class EmptyReferenceChecker(ReferenceChecker):
    def __init__(self):
        exclusion_list = []
        index_patterns = [r""]    
        text_pattern = ""

        super().__init__(regex_list_of_indices = index_patterns, text_version = text_pattern, exclusion_list=exclusion_list)
        self.text_version = text_pattern

    def is_valid(self, reference):
        if reference == None or reference == "":
            return True
        if reference == "all":
            return True
        return False

    def extract_valid_reference(self, input_string):
        return ""
    
    def split_reference(self, reference):
        return ""

    def get_parent_reference(self, input_string):
        return ""

    def get_current_and_parent_references(self, reference):
        return [""]

    def is_reference_or_parents_in_list(self, reference, list_of_references):
        super().is_reference_or_parents_in_list(reference, list_of_references) 

    def _extract_reference_from_string(self, s):
        return ""

