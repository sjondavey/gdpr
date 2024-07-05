import pandas as pd
from openai import OpenAI
import os
from cryptography.fernet import Fernet

from regulations_rag.corpus_chat import ChatParameters
from regulations_rag.embeddings import  EmbeddingParameters
from regulations_rag.file_tools import load_parquet_data
from regulations_rag.rerank import RerankAlgos

from regulations_rag.corpus import Corpus
from regulations_rag.corpus_chat import CorpusChat
from gdpr_rag.corpus_index import GDPRCorpusIndex

class TestRegulationChat:
    include_calls_to_api = True
    openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"),)
    chat_parameters = ChatParameters(chat_model = "gpt-4o", temperature = 0, max_tokens = 500)

    embedding_parameters = EmbeddingParameters("text-embedding-3-large", 1024)
    key = os.getenv('encryption_key_gdpr')


    corpus_index = GDPRCorpusIndex(key)


    chat = CorpusChat(openai_client = openai_client, 
                      embedding_parameters = embedding_parameters, 
                      chat_parameters = chat_parameters, 
                      corpus_index = corpus_index,
                      rerank_algo = RerankAlgos.MOST_COMMON,   
                      user_name_for_logging = 'test_user')

    def test_construction(self):
        assert True


    def test_resource_augmented_query(self):
        self.chat.reset_conversation_history()
        self.chat.system_state = self.chat.State.RAG

        user_content = "Are there exemptions from GDPR for small companies?"
        workflow_triggered, relevant_definitions, relevant_sections = self.chat.similarity_search(user_content)

        if self.include_calls_to_api: # also test it with a call to the API
            result = self.chat.resource_augmented_query(user_question = user_content,
                                                          df_definitions = relevant_definitions, 
                                                          df_search_sections = relevant_sections)
            assert result["success"]
            assert result["path"] == "ANSWER:"
            #assert result["answer"] == "test to see what happens when if the API believes it successfully answered the question with the resources provided"
            assert len(result["reference"]) > 0


            # Manually force the first API response to get to the second loop, then test the second API call
            # NOTE: I am not going to test the openai api call. I am going to use 'testing' mode with canned answers
            testing = True
            manual_responses_for_testing = []
            manual_responses_for_testing.append("Yes. There are exemptions for small companies.")
            result = self.chat.resource_augmented_query(user_question = "Are there exemptions from GDPR for small companies?", 
                                                        df_definitions = relevant_definitions, 
                                                        df_search_sections = relevant_sections,
                                                        testing = testing,
                                                        manual_responses_for_testing = manual_responses_for_testing)
            assert result["success"]
            assert result["path"] == "ANSWER:"
            #assert result["answer"] == "test to see what happens when if the API believes it successfully answered the question with the resources provided"
            assert len(result["reference"]) > 0


