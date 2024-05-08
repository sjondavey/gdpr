from gdpr_rag.documents.gdpr import GDPR
from gdpr_rag.documents.article_30_5 import Article_30_5
from gdpr_rag.documents.article_47_bcr import Article_47_BCR


from regulations_rag.corpus import Corpus, create_document_dictionary_from_folder


class GDPRCorpus(Corpus):
    def __init__(self, folder):
        #tmp = find_class_names_in_files(folder)
        document_dictionary = create_document_dictionary_from_folder(folder, globals())
        super().__init__(document_dictionary)

# def create_document_dictionary_from_folder(folder_name):
#     """
#     Create a dictionary of document instances from Python classes defined in the files within a given folder.

#     Args:
#     folder_name (str): The name of the folder where the Python files are located.

#     Returns:
#     dict: A dictionary where keys are the class names and values are instances of these classes.

#     This function reads Python files in the specified folder, extracts class definitions, and creates an instance
#     of each class. 
#     """
#     class_names_dict = find_class_names_in_files(folder_name)
#     all_documents = {}
#     for class_name in class_names_dict:

#         doc_class = get_document_class_by_name(class_names_dict[class_name])
#         if doc_class:
#             document_instance = doc_class()
#             all_documents[class_names_dict[class_name]] = document_instance
#     return all_documents
