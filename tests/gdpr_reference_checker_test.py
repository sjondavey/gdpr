import pytest
from gdpr_rag.gdpr_reference_checker import GDPRReferenceChecker

class TestGDPRReferenceChecker:

    reference_checker = GDPRReferenceChecker()

    def test_is_valid(self):
        blank_reference = ""
        assert not self.reference_checker.is_valid(blank_reference)

        reference = '14(1)(a)'
        assert self.reference_checker.is_valid(reference)
        very_long_reference = '14(1)(a)(i)'
        assert not self.reference_checker.is_valid(very_long_reference)

        short_reference = '98'        
        assert self.reference_checker.is_valid(short_reference)

        invalid_reference = '41(a)'
        assert not self.reference_checker.is_valid(invalid_reference)


    def test_extract_valid_reference(self):
        assert self.reference_checker.extract_valid_reference(' 14 some heading here (1) another heading here (a)') == '14(1)(a)'

    def test_split_reference(self):

        short_reference = '14(1)(a)'        
        components = self.reference_checker.split_reference(short_reference)
        assert len(components) == 3
        assert components[0] == '14'
        assert components[1] == '(1)'
        assert components[2] == '(a)'


        invalid_reference = '14(i)(a)'
        with pytest.raises(ValueError):
            components = self.reference_checker.split_reference(invalid_reference)


    # def test_get_parent_reference(self):
    #     reference = 'G.1(C)(xviii)(c)(dd)(9)'
    #     assert self.reference_checker.get_parent_reference(reference) == 'G.1(C)(xviii)(c)(dd)'
    #     with pytest.raises(ValueError):
    #         components = self.reference_checker.get_parent_reference("")

    # def test_get_current_and_parent_references(self):
    #     reference = 'G.1(C)(xviii)(c)(dd)(9)'
    #     current_and_parent = ['G.1(C)(xviii)(c)(dd)(9)', 'G.1(C)(xviii)(c)(dd)', 'G.1(C)(xviii)(c)', 'G.1(C)(xviii)', 'G.1(C)', 'G.1']
    #     assert self.reference_checker.get_current_and_parent_references(reference) == current_and_parent

    # def test_is_reference_or_parents_in_list(self):
    #     reference = 'G.1(C)(xviii)(c)(dd)(9)'
    #     list_of_references = ['A.1', 'B.1', 'C.1']
    #     assert not self.reference_checker.is_reference_or_parents_in_list(reference, list_of_references)
    #     list_of_references = ['A.1', 'B.1', 'G.1']
    #     assert self.reference_checker.is_reference_or_parents_in_list(reference, list_of_references)
        

    # def test___extract_reference_from_string(self):
    #     string_with_no_reference = 'Africa means any country forming part of the African Union.'
    #     index, string = self.reference_checker._extract_reference_from_string(string_with_no_reference)
    #     assert index == ""
    #     assert string == string_with_no_reference

    #     # tests for each of the numbering patters used in excon_index_patterns
    #     string_with_reference = 'A.1 Definitions'
    #     index, string = self.reference_checker._extract_reference_from_string(string_with_reference)
    #     assert index == "A.1"
    #     assert string == 'Definitions'

    #     string_with_reference = '(A) Authorised Dealers'
    #     index, string = self.reference_checker._extract_reference_from_string(string_with_reference)
    #     assert index == "(A)"
    #     assert string == 'Authorised Dealers'

    #     string_with_reference = '(xxiii) Authorised Dealers must reset their application numbering systems to zero at the beginning of each calendar year.'
    #     index, string = self.reference_checker._extract_reference_from_string(string_with_reference)
    #     assert index == "(xxiii)"
    #     assert string == 'Authorised Dealers must reset their application numbering systems to zero at the beginning of each calendar year.'

    #     string_with_reference = '(a) a list of application numbers generated but not submitted to the Financial Surveillance Department;'
    #     index, string = self.reference_checker._extract_reference_from_string(string_with_reference)
    #     assert index == "(a)"
    #     assert string == 'a list of application numbers generated but not submitted to the Financial Surveillance Department;'

    #     string_with_reference = '(dd) CMA residents who travel overland to and from other CMA countries through a SADC country up to an amount not exceeding R25 000 per calendar year. This allocation does not form part of the permissible travel allowance for residents; and'
    #     index, string = self.reference_checker._extract_reference_from_string(string_with_reference)
    #     assert index == "(dd)"
    #     assert string == 'CMA residents who travel overland to and from other CMA countries through a SADC country up to an amount not exceeding R25 000 per calendar year. This allocation does not form part of the permissible travel allowance for residents; and'

    #     string_with_reference = '(1) the full names and identity number of the applicant;'
    #     index, string = self.reference_checker._extract_reference_from_string(string_with_reference)
    #     assert index == "(1)"
    #     assert string == 'the full names and identity number of the applicant;'

    #     heading_on_exclusion_list = 'Legal context'
    #     index, string = self.reference_checker._extract_reference_from_string(heading_on_exclusion_list)
    #     assert index == heading_on_exclusion_list
    #     assert string == ""
