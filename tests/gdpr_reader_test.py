import pytest
import pandas as pd

from gdpr_rag.gdpr_reference_checker import GDPRReferenceChecker

from gdpr_rag.gdpr_reader import  GDPRReader


#reference_checker = gdprReferenceChecker()

#df = pd.read_csv("./inputs/ad_manual.csv", sep="|", encoding="utf-8", na_filter="")
#df = load_regulation_data_from_files("./inputs/ad_manual.csv", "./inputs/ad_manual_plus.csv")
test_reader = GDPRReader()

def test_get_regulation_detail():
    response = test_reader.get_regulation_detail('14(1)(a)')
    expected_response = "Article 14 Information to be provided where personal data have not been obtained from the data subject\n    1. Where personal data have not been obtained from the data subject, the controller shall provide the data subject with the following information:\n        (a) the identity and the contact details of the controller and, where applicable, of the controller's representative;\n"
    assert response == expected_response


def test_get_regulation_heading():
    response = test_reader.get_regulation_heading('14(1)(a)')
    expected_response = 'Chapter III Rights of the data subject\nSection 2 Information and access to personal data\nArticle 14 Information to be provided where personal data have not been obtained from the data subject\n'
    assert response == expected_response

