
from regulations_rag.regulation_index import EmbeddingParameters
from regulations_rag.regulation_chat import RegulationChat, ChatParameters
from regulations_rag.rerank import RerankAlgos

from gdpr_rag.gdpr_reference_checker import GDPRReferenceChecker
from gdpr_rag.gdpr_index import GDPRIndex
from gdpr_rag.gdpr_reader import GDPRReader

class GDPRChat(RegulationChat):
    def __init__(self, openai_client, decryption_key, rerank_algo = RerankAlgos.MOST_COMMON, user_name_for_logging = 'test_user'):
        chat_parameters = ChatParameters(chat_model = "gpt-4-0125-preview", temperature = 0, max_tokens = 500)
        #model_to_use = "gpt-3.5-turbo"
        #model_to_use = "gpt-4-1106-preview"
        #model_to_use="gpt-3.5-turbo-16k"

        embedding_parameters = EmbeddingParameters("text-embedding-3-large", 1024)

        index = GDPRIndex(decryption_key)
        reader = GDPRReader()

        
        reference_checker = GDPRReferenceChecker()



        #rerank_algo = RerankAlgos.MOST_COMMON
        if rerank_algo == RerankAlgos.LLM:
            rerank_algo.params["openai_client"] = openai_client
            rerank_algo.params["model_to_use"] = chat_parameters.model


        super().__init__(openai_client = openai_client, 
                          embedding_parameters = embedding_parameters, 
                          chat_parameters = chat_parameters, 
                          regulation_reader = reader, 
                          regulation_index = index,
                          rerank_algo = rerank_algo,   
                          user_name_for_logging = 'test_user')
        

    # def reformat_assistant_answer(self, raw_response, sections_in_rag):
    #     # # Early return if no references found. This can happen if the answer is in the definitions for example
    #     # if not sections_in_rag:
    #     #     return raw_response

    #     # # Extract and clean references from the raw response
    #     # references = raw_response.split("Reference:")[1].split(",") if "Reference:" in raw_response else []
    #     # cleaned_references = [ref.strip() for ref in references if ref.strip()]

    #     # # Early return if no references found
    #     # if not cleaned_references:
    #     #     return raw_response.split("Reference:")[0].strip()

    #     # unique_references = match_strings_to_reference_list(cleaned_references, sections_in_rag)

    #     # # Get headings for matched references
    #     # reference_headings = [self.reader.get_regulation_heading(ref) for ref in unique_references]

    #     # # Reconstruct the answer with reformatted references
    #     # answer_base = raw_response.split("Reference:")[0].strip()
    #     # formatted_references = "  \nReference:" + "".join(f"  \n{ref}: {heading}" for ref, heading in zip(unique_references, reference_headings))

    #     # return unique_references, answer_base + formatted_references
    #     return sections_in_rag, raw_response
