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

from regulations_rag.path_search import PathSearch
from regulations_rag.path_rag import PathRAG
from regulations_rag.data_classes import AnswerWithRAGResponse, AnswerWithoutRAGResponse
from regulations_rag.corpus_chat_tools import get_caveat_for_no_rag_response

class TestRegulationChat:
    include_calls_to_api = True
    api_key=os.environ.get("OPENAI_API_KEY")
    # openai_client = OpenAI(api_key=api_key,) # moved to chat_parameters

    chat_parameters = ChatParameters(chat_model = "gpt-4o",  
                                     api_key=api_key, 
                                     temperature = 0, 
                                     max_tokens = 500, 
                                     token_limit_when_truncating_message_queue = 3500)

    embedding_parameters = EmbeddingParameters("text-embedding-3-large", 1024)
    key = os.getenv('encryption_key_gdpr')


    corpus_index = GDPRCorpusIndex(key)


    chat = CorpusChat(embedding_parameters = embedding_parameters, 
                      chat_parameters = chat_parameters, 
                      corpus_index = corpus_index,
                      rerank_algo = RerankAlgos.MOST_COMMON,   
                      user_name_for_logging = 'test_user')

    def test_construction(self):
        assert True


    @patch.object(ChatParameters, 'get_api_response')
    def test_resource_augmented_query(self, mock_get_api_response):
        self.chat.reset_conversation_history()
        self.chat.system_state = self.chat.State.RAG

        user_content = "Are there exemptions from GDPR for small companies?"

        path_search = PathSearch(corpus_index = self.corpus_index, 
                                 chat_parameters = self.chat_parameters, 
                                 embedding_parameters = self.embedding_parameters, 
                                 rerank_algo = RerankAlgos.MOST_COMMON)

        workflow_triggered, relevant_definitions, relevant_sections = path_search.similarity_search(user_question=user_content)

        mock_get_api_response.return_value = "ANSWER: There are exemptions for small companies."

        path_rag = PathRAG(corpus_index = self.corpus_index, 
                           chat_parameters = self.chat_parameters)
    
        message_history = []
        current_user_message = {"content": user_content, 
                    "reference_material": {"definitions": relevant_definitions, 
                                            "sections": relevant_sections}} 

        result = path_rag.perform_RAG_path(message_history=message_history, 
                                           current_user_message=current_user_message)
        assert isinstance(result["assistant_response"], AnswerWithoutRAGResponse)
        assert result["role"] == "assistant"
        assert result["content"] == get_caveat_for_no_rag_response() + " \n\nThere are exemptions for small companies."

        # Check that that the system initially does not listen, that it makes it to the second step: 
        mock_get_api_response.side_effect = [
            "Yes. There are exemptions for small companies.", 
            "ANSWER: After checking my previous answer, there are exemptions for small companies."
            ]

        result = path_rag.perform_RAG_path(message_history=message_history, 
                                           current_user_message=current_user_message)
        
        assert isinstance(result["assistant_response"], AnswerWithoutRAGResponse)
        assert result["role"] == "assistant"
        assert result["content"] == get_caveat_for_no_rag_response() + " \n\nAfter checking my previous answer, there are exemptions for small companies."


