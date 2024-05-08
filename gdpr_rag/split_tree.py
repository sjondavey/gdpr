import pandas as pd
from regulations_rag.embeddings import num_tokens_from_string

from regulations_rag.regulation_table_of_content import StandardTableOfContent
from gdpr_rag.document import Document

def _split_recursive(node, regulation_reader, table_of_content, token_limit, node_list=[]):
    """    
    Recursively splits nodes based on token limits and collects valid nodes in a list.
    You shouldn't need to call this method. Rather use the "split_tree()" method
    
    Parameters:
    - node (Node): The current node being processed.
    - dataframe (pd.DataFrame): DataFrame containing the regulation details.
    - token_limit (int): The maximum allowed token count per section.
    - index_checker (callable): Function to check if an index is valid.
    - node_list (list, optional): List to collect nodes meeting the token criteria.
    
    Returns:
    - list: A list of nodes that meet the token criteria.
    """
    if node_list is None:
        node_list = []

    subsection_text = regulation_reader.get_text(node.full_node_name)
    token_count = num_tokens_from_string(subsection_text)

    if token_count > token_limit:
        if not node.children:
            raise Exception(f'Node {node.full_node_name} has no children but has a token count of {token_count} so it cannot be split into nodes that contain fewer tokens that {token_limit}')
        for child in node.children:
            _split_recursive(child, regulation_reader, table_of_content, token_limit, node_list)
    else:
        node_list.append(node)

    return node_list


def split_tree(node, regulation_reader, table_of_content, token_limit):
    """
    Splits a tree starting from a given node into sections that don't exceed a token limit.
    
    Initially this is used to set up the base DataFrame using node == root and later it can be used if we want 
    to change the word_limit for a specific piece of regulation to change chunking where it makes sense.

    Parameters:
    - node (Node): The starting node to split the tree.
    - dataframe (pd.DataFrame): DataFrame containing regulation details.
    - token_limit (int): The maximum allowed token count per section.
    - index_checker (callable): Function to check if an index is valid.
    
    Returns:
    - pd.DataFrame: A DataFrame with columns ['section_reference', 'text', 'token_count'] for each valid section_reference.
    """
    node_list = _split_recursive(node, regulation_reader, table_of_content, token_limit, node_list=[])
    section_token_count = [[node.full_node_name, 
                            regulation_reader.get_text(node.full_node_name),
                            num_tokens_from_string(regulation_reader.get_text(node.full_node_name))] 
                           for node in node_list]


    return pd.DataFrame(section_token_count, columns=['section_reference', 'text', 'token_count'])


