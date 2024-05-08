from gdpr_rag.documents.gdpr import GDPR

import sys
sys.path.append('E:/Code/chat/gdpr')


def test_regression():
    path_to_manual_as_csv_file = "./inputs/documents/gdpr.csv"

    doc = GDPR(path_to_manual_as_csv_file)
    section = "all"
    assert doc.get_heading(section) == ""
    assert doc.get_text(section) == ''

    section = "3"
    assert doc.get_heading(section) == 'Chapter I General provisions. Article 3 Territorial scope.'
    assert doc.get_text(section) == '3 Territorial scope\n    1. This Regulation applies to the processing of personal data in the context of the activities of an establishment of a controller or a processor in the Union, regardless of whether the processing takes place in the Union or not.\n    2. This Regulation applies to the processing of personal data of data subjects who are in the Union by a controller or processor not established in the Union, where the processing activities are related to:\n        (a) the offering of goods or services, irrespective of whether a payment of the data subject is required, to such data subjects in the Union; or\n        (b) the monitoring of their behaviour as far as their behaviour takes place within the Union.\n    3. This Regulation applies to the processing of personal data by a controller not established in the Union, but in a place where Member State law applies by virtue of public international law.\n'

    section = "2"
    assert doc.get_heading(section) == 'Chapter I General provisions. Article 2 Material scope.'
    assert doc.get_text(section) == '2 Material scope\n    1. This Regulation applies to the processing of personal data wholly or partly by automated means and to the processing other than by automated means of personal data which form part of a filing system or are intended to form part of a filing system.\n    2. This Regulation does not apply to the processing of personal data:\n        (a) in the course of an activity which falls outside the scope of Union law;\n        (b) by the Member States when carrying out activities which fall within the scope of Chapter 2 of Title V of the TEU;\n        (c) by a natural person in the course of a purely personal or household activity;\n        (d) by competent authorities for the purposes of the prevention, investigation, detection or prosecution of criminal offences or the execution of criminal penalties, including the safeguarding against and the prevention of threats to public security.\n    3. For the processing of personal data by the Union institutions, bodies, offices and agencies, Regulation (EC) No 45/2001 applies. Regulation (EC) No 45/2001 and other Union legal acts applicable to such processing of personal data shall be adapted to the principles and rules of this Regulation in accordance with Article 98.\n    4. This Regulation shall be without prejudice to the application of Directive 2000/31/EC, in particular of the liability rules of intermediary service providers in Articles 12 to 15 of that Directive.\n'

    
    section = "3(2)(b)"
    assert doc.get_heading(section) == 'Chapter I General provisions. Article 3 Territorial scope.'
    assert doc.get_text(section) == '3 Territorial scope\n    2. This Regulation applies to the processing of personal data of data subjects who are in the Union by a controller or processor not established in the Union, where the processing activities are related to:\n        (b) the monitoring of their behaviour as far as their behaviour takes place within the Union.\n'

