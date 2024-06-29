import os
import pandas as pd
from openai import OpenAI
from gdpr_rag.corpus_index import GDPRCorpusIndex
from regulations_rag.embeddings import get_ada_embedding, EmbeddingParameters
from regulations_rag.rerank import RerankAlgos

class TestGDPRCorpusIndex():

    key = os.getenv('encryption_key_gdpr')
    index = GDPRCorpusIndex(key)
    openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"),)
    embedding_parameters = EmbeddingParameters("text-embedding-3-large", 1024)

    def test_construction(self):
        assert True

    def test_get_relevant_definitions(self):
        user_content = "what is a controller?"
        user_content_embedding = get_ada_embedding(self.openai_client, user_content, self.embedding_parameters.model, self.embedding_parameters.dimensions)       
        relevant_definitions = self.index.get_relevant_definitions(user_content = user_content, user_content_embedding = user_content_embedding, threshold = self.embedding_parameters.threshold) 
        assert len(relevant_definitions) == 1
        section = relevant_definitions.iloc[0]["section_reference"]
        assert section == "4(7)"
        doc = relevant_definitions.iloc[0]["document"]
        assert doc == "GDPR"
        definition = self.index.corpus.get_text(doc, section, add_markdown_decorators = False)
        expected_definition = "4 Definitions\n    7. 'controller' means the natural or legal person, public authority, agency or other body which, alone or jointly with others, determines the purposes and means of the processing of personal data; where the purposes and means of such processing are determined by Union or Member State law, the controller or the specific criteria for its nomination may be provided for by Union or Member State law;\n"
        assert definition == expected_definition 

    def test_get_relevant_sections(self):
        user_content = "Are there exemptions from GDPR for small companies?"
        user_content_embedding = get_ada_embedding(self.openai_client, user_content, self.embedding_parameters.model, self.embedding_parameters.dimensions)     
        rerank_algo = RerankAlgos.NONE  
        relevant_definitions = self.index.get_relevant_sections(user_content = user_content, user_content_embedding = user_content_embedding, threshold = self.embedding_parameters.threshold, rerank_algo=rerank_algo) 
        assert len(relevant_definitions) == 5
        documents_that_are_referenced = relevant_definitions['document'].unique()
        assert "GDPR" in documents_that_are_referenced
        assert "Article_30_5" in documents_that_are_referenced
        indices = relevant_definitions[relevant_definitions['document'] == "Article_30_5"].index.tolist()
        article = relevant_definitions.iloc[indices[0]]["regulation_text"]
        expected_article = '\nThe Working Party 29 has examined the obligation, under Article 30 of the GDPR, for controllers and processors to maintain a record of processing activities. This paper sets out the WP29\'s position on the derogation from this obligation. Recital 13 of the GDPR says:\n\'To take account of the specific situation of micro, small and medium-sized enterprises, this Regulation includes a derogation for organisations with fewer than 250 employees with regard to record-keeping\'.\nArticle 30(5) gives effect to Recital 13. It says that the obligation to keep a record of processing activities does not apply \'to an enterprise or an organisation employing fewer than 250 persons unless the processing it carries out is likely to result in a risk to the rights and freedoms of data subjects, the processing is not occasional, or the processing includes special categories of data as referred to in Article 9(1) or personal data relating to criminal convictions and offences referred to in Article 10.\' Some clarifications on the interpretation of this provision appear necessary, as shown by the high number of requests coming from companies and received in the last few months by national Supervisory Authorities.\nThe derogation provided by Article 30(5) is not absolute. There are three types of processing to which it does not apply. These are:\n·         Processing that is likely to result in a risk to the rights and freedoms of data subjects.\n·         Processing that is not occasional.\n·         Processing that includes special categories of data or personal data relating to criminal convictions and offences.\n\nThe WP29 underlines that the wording of Article 30(5) is clear in providing that the three types of processing to which the derogation does not apply are alternative ("or") and the occurrence of any one of them alone triggers the obligation to maintain the record of processing activities.\nTherefore, although endowed with less than 250 employees, data controllers or processors who find themselves in the position of either carrying out processing likely to result in a risk (not just a high risk) to the rights of the data subjects, or processing personal data on a non-occasional basis, or processing special categories of data under Article 9(1) or data relating to criminal convictions under Article 10 are obliged to maintain the record of processing activities. \nHowever, such organisations need only maintain records of processing activities for the types of processing mentioned by Article 30(5).\nFor example, a small organisation is likely to regularly process data regarding its employees. As a result, such processing cannot be considered "occasional" and must therefore be included in the record of processing activities.1 Other processing activities which are in fact "occasional", however, do not need to be included in the record of processing activities, provided they are unlikely to result in a risk to the right and freedoms of data subjects and do not involve special categories of data or personal data relating to criminal convictions and offences.\nThe WP29 highlights that the record of processing activities is a very useful means to support an analysis of the implications of any processing whether existing or planned. The record facilitates the factual assessment of the risk of the processing activities performed by a controller or processor on individuals\' rights, and the identification and implementation of appropriate security measures to safeguard personal data – both key components of the principle of accountability contained in the GDPR.\nFor many micro, small and medium-sized organisations, maintaining a record of processing activities is unlikely to constitute a particularly heavy burden. However, the WP29 recognises that Article 30 represents a new administrative requirement for controllers and processors, and therefore encourages national Supervisory Authorities to support SMEs by providing tools to facilitate the set up and management of records of processing activities. For example, a Supervisory Authority might make available on its website a simplified model that can be used by SMEs to keep records of processing activities not covered by the derogation in Article 30(5).\n\n\n1 The WP29 considers that a processing activity can only be considered as "occasional" if it is not carried out regularly, and occurs outside the regular course of business or activity of the controller or processor. See WP29 Guidelines on Article 49 of Regulation 2016/679 (WP262). \n'
        assert article == expected_article

