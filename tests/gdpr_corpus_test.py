import pytest
from gdpr_rag.gdpr_corpus import GDPRCorpus


class TestGDPRCorpus():

    corpus = GDPRCorpus("./gdpr_rag/documents/")

    def test_construction(self):
        doc = self.corpus.get_document('GDPR')
        art = doc.get_text('2', add_markdown_decorators = False)

        expected_answer = '2 Material scope\n    1. This Regulation applies to the processing of personal data wholly or partly by automated means and to the processing other than by automated means of personal data which form part of a filing system or are intended to form part of a filing system.\n    2. This Regulation does not apply to the processing of personal data:\n        (a) in the course of an activity which falls outside the scope of Union law;\n        (b) by the Member States when carrying out activities which fall within the scope of Chapter 2 of Title V of the TEU;\n        (c) by a natural person in the course of a purely personal or household activity;\n        (d) by competent authorities for the purposes of the prevention, investigation, detection or prosecution of criminal offences or the execution of criminal penalties, including the safeguarding against and the prevention of threats to public security.\n    3. For the processing of personal data by the Union institutions, bodies, offices and agencies, Regulation (EC) No 45/2001 applies. Regulation (EC) No 45/2001 and other Union legal acts applicable to such processing of personal data shall be adapted to the principles and rules of this Regulation in accordance with Article 98.\n    4. This Regulation shall be without prejudice to the application of Directive 2000/31/EC, in particular of the liability rules of intermediary service providers in Articles 12 to 15 of that Directive.\n'
        assert art == expected_answer

        txt = self.corpus.get_text('GDPR', '2', add_markdown_decorators = False)
        assert txt == expected_answer

        txt = self.corpus.get_text('Article_30_5', 'all', add_markdown_decorators = False)
        expected_answer = '\nThe Working Party 29 has examined the obligation, under Article 30 of the GDPR, for controllers and processors to maintain a record of processing activities. This paper sets out the WP29\'s position on the derogation from this obligation. Recital 13 of the GDPR says:\n\'To take account of the specific situation of micro, small and medium-sized enterprises, this Regulation includes a derogation for organisations with fewer than 250 employees with regard to record-keeping\'.\nArticle 30(5) gives effect to Recital 13. It says that the obligation to keep a record of processing activities does not apply \'to an enterprise or an organisation employing fewer than 250 persons unless the processing it carries out is likely to result in a risk to the rights and freedoms of data subjects, the processing is not occasional, or the processing includes special categories of data as referred to in Article 9(1) or personal data relating to criminal convictions and offences referred to in Article 10.\' Some clarifications on the interpretation of this provision appear necessary, as shown by the high number of requests coming from companies and received in the last few months by national Supervisory Authorities.\nThe derogation provided by Article 30(5) is not absolute. There are three types of processing to which it does not apply. These are:\n·         Processing that is likely to result in a risk to the rights and freedoms of data subjects.\n·         Processing that is not occasional.\n·         Processing that includes special categories of data or personal data relating to criminal convictions and offences.\n\nThe WP29 underlines that the wording of Article 30(5) is clear in providing that the three types of processing to which the derogation does not apply are alternative ("or") and the occurrence of any one of them alone triggers the obligation to maintain the record of processing activities.\nTherefore, although endowed with less than 250 employees, data controllers or processors who find themselves in the position of either carrying out processing likely to result in a risk (not just a high risk) to the rights of the data subjects, or processing personal data on a non-occasional basis, or processing special categories of data under Article 9(1) or data relating to criminal convictions under Article 10 are obliged to maintain the record of processing activities. \nHowever, such organisations need only maintain records of processing activities for the types of processing mentioned by Article 30(5).\nFor example, a small organisation is likely to regularly process data regarding its employees. As a result, such processing cannot be considered "occasional" and must therefore be included in the record of processing activities.1 Other processing activities which are in fact "occasional", however, do not need to be included in the record of processing activities, provided they are unlikely to result in a risk to the right and freedoms of data subjects and do not involve special categories of data or personal data relating to criminal convictions and offences.\nThe WP29 highlights that the record of processing activities is a very useful means to support an analysis of the implications of any processing whether existing or planned. The record facilitates the factual assessment of the risk of the processing activities performed by a controller or processor on individuals\' rights, and the identification and implementation of appropriate security measures to safeguard personal data – both key components of the principle of accountability contained in the GDPR.\nFor many micro, small and medium-sized organisations, maintaining a record of processing activities is unlikely to constitute a particularly heavy burden. However, the WP29 recognises that Article 30 represents a new administrative requirement for controllers and processors, and therefore encourages national Supervisory Authorities to support SMEs by providing tools to facilitate the set up and management of records of processing activities. For example, a Supervisory Authority might make available on its website a simplified model that can be used by SMEs to keep records of processing activities not covered by the derogation in Article 30(5).\n\n\n1 The WP29 considers that a processing activity can only be considered as "occasional" if it is not carried out regularly, and occurs outside the regular course of business or activity of the controller or processor. See WP29 Guidelines on Article 49 of Regulation 2016/679 (WP262). \n'
        assert txt == expected_answer

        assert doc.reference_checker.is_valid('2')
            