import pandas as pd
from openai import OpenAI
import os
from unittest.mock import patch

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


    @patch.object(CorpusChat, 'get_api_response')
    def test_resource_augmented_query(self, mock_get_api_response):
        self.chat.reset_conversation_history()
        self.chat.system_state = self.chat.State.RAG

        user_content = "Are there exemptions from GDPR for small companies?"
        workflow_triggered, relevant_definitions, relevant_sections = self.chat.similarity_search(user_content)

        mock_get_api_response.return_value = "ANSWER: There are exemptions for small companies."
        result = self.chat.resource_augmented_query(user_question = user_content,
                                                        df_definitions = relevant_definitions, 
                                                        df_search_sections = relevant_sections)
        assert result["success"]
        assert result["path"] == "ANSWER:"
        assert result["answer"] == "There are exemptions for small companies."
        assert len(result["reference"]) == 0

        # Check that that the system initially does not listen, that it makes it to the second step: 
        mock_get_api_response.side_effect = [
            "Yes. There are exemptions for small companies.", 
            "ANSWER: After checking my previous answer, there are exemptions for small companies."
            ]

        result = self.chat.resource_augmented_query(user_question = "Are there exemptions from GDPR for small companies?", 
                                                    df_definitions = relevant_definitions, 
                                                    df_search_sections = relevant_sections)
        assert result["success"]
        assert result["path"] == "ANSWER:"
        assert result["answer"] == "After checking my previous answer, there are exemptions for small companies."
        assert len(result["reference"]) == 0


