from regulations_rag.reference_checker import ReferenceChecker

class GDPRReferenceChecker(ReferenceChecker):
    def __init__(self):
        exclusion_list = []

        gdpr_index_patterns = [
            r'^\d{1,2}',   # Matches numbers, excluding leading zeros. - Article Number
            r'^\((?:[1-9]|[1-9][0-9])\)',   # Matches numbers within parentheses, excluding leading zeros. 
            r'^\([a-z]\)',                  # Matches single lowercase letters within parentheses.
        ]
        
        # ^Article : Matches the beginning of the string, followed by "Article ". - mandatory
        # (\d{1,2}): Captures a one or two digit number immediately following "Article ". - mandatory
        # (?:\((\d{1,2})\))?: An optional non-capturing group that contains a capturing group for a one or two digit number enclosed in parentheses. The entire group is made optional by ?, so it matches 0 or 1 times.
        # (?:\(([a-z])\))?: Another optional non-capturing group that contains a capturing group for a single lowercase letter enclosed in parentheses. This part is also optional.
        text_pattern = r'^(\d{1,2})(?:\((\d{1,2})\))?(?:\(([a-z])\))?'

        super().__init__(regex_list_of_indices = gdpr_index_patterns, text_version = text_pattern, exclusion_list=exclusion_list)
