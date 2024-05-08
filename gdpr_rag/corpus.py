import logging
import os
import ast

from gdpr_rag.documents.gdpr import GDPR
from gdpr_rag.documents.article_30_5 import Article_30_5
from gdpr_rag.documents.article_47_bcr import Article_47_BCR

logger = logging.getLogger(__name__)
DEV_LEVEL = 15
logging.addLevelName(DEV_LEVEL, 'DEV')       

def find_class_names_in_files(directory):
    class_dict = {}
    for filename in os.listdir(directory):
        if filename.endswith(".py"):  # Check for Python files
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as file:
                file_content = file.read()
            tree = ast.parse(file_content)
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    class_name = node.name
                    file_name_without_extension = os.path.splitext(filename)[0]
                    class_dict[file_name_without_extension] = class_name
                    break  # Assuming one class per file, break after finding the first class
    return class_dict

# Usage



def get_document_class_by_name(class_name):
    return globals().get(class_name)


class Corpus():
    def __init__(self, folder_name):
        class_names_dict = find_class_names_in_files(folder_name)
        self.all_documents = {}
        for class_name in class_names_dict:

            doc_class = get_document_class_by_name(class_names_dict[class_name])
            if doc_class:
                document_instance = doc_class()
                self.all_documents[class_names_dict[class_name]] = document_instance
                #self.all_documents[class_name] = document_instance
                logger.log(DEV_LEVEL, f"Added instance of {class_name} to all_documents.")
            else:
                logger.log(DEV_LEVEL, f"Class {class_name} not found.")

    def get_document(self, document_name):
        return self.all_documents.get(document_name)

    def get_heading(self, document_name, section_reference):
        doc = self.get_document(document_name)
        return doc.get_heading(section_reference)

    def get_text(self, document_name, section_reference):
        doc = self.get_document(document_name)
        return doc.get_text(section_reference)
