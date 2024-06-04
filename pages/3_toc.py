import streamlit_antd_components as sac
from anytree import Node, RenderTree
from regulations_rag.regulation_table_of_content import StandardTableOfContent

from gdpr_rag.documents.gdpr import GDPR


doc = GDPR()
df = doc.document_as_df

import pandas as pd
gdpr_data_for_tree = []
chapter_number = ""
article_number = 0

for index, row in df.iterrows():
    if row["chapter_number"] != chapter_number:
        chapter_number = row["chapter_number"]
        section_number = ""
        gdpr_data_for_tree.append([row["chapter_number"], True, row["chapter_heading"]])

    if row["article_number"] != article_number:
        article_number = row["article_number"]
        gdpr_data_for_tree.append([f'{chapter_number}.{row["article_number"]}', True, row["article_heading"]])

gdpr_df_for_tree = pd.DataFrame(gdpr_data_for_tree, columns = ["section_reference", "heading", "text"])

from regulations_rag.reference_checker import ReferenceChecker
class GDPRTreeReferenceChecker(ReferenceChecker):
    def __init__(self):
        exclusion_list = []

        gdpr_index_patterns = [
            r'^\b(I|II|III|IV|V|VI|VII|VIII|IX|X|XI)\b',
            r'^\.\d{1,2}',   # Matches numbers, excluding leading zeros. - Article Number
        ]
        
        # ^Article : Matches the beginning of the string, followed by "Article ". - mandatory
        # (\d{1,2}): Captures a one or two digit number immediately following "Article ". - mandatory
        # (?:\((\d{1,2})\))?: An optional non-capturing group that contains a capturing group for a one or two digit number enclosed in parentheses. The entire group is made optional by ?, so it matches 0 or 1 times.
        # (?:\(([a-z])\))?: Another optional non-capturing group that contains a capturing group for a single lowercase letter enclosed in parentheses. This part is also optional.
        text_pattern = r'((I|II|III|IV|V|VI|VII|VIII|IX|X|XI))(?:\((\d{1,2})\))?'

        super().__init__(regex_list_of_indices = gdpr_index_patterns, text_version = text_pattern, exclusion_list=exclusion_list)


toc = StandardTableOfContent(root_node_name = doc.name, index_checker = GDPRTreeReferenceChecker(), regulation_df = gdpr_df_for_tree)

def anytree_to_treeitem(node):
    if node.full_node_name == '':
        return sac.TreeItem(
        label= f'{node.name}',
        children=[anytree_to_treeitem(child) for child in node.children] if node.children else None
        )
    else: 
        return sac.TreeItem(
            label= f'{node.full_node_name} {node.heading_text}',
            children=[anytree_to_treeitem(child) for child in node.children] if node.children else None
        )

# Convert the anytree structure to a list of dictionaries
tree_data = [anytree_to_treeitem(toc.root)]
# Display the tree using sac.tree
sac.tree(items=tree_data, label='Included Documents', index=0, size='md')

# for doc in included_docs:

#     reference_checker = doc.reference_checker
#     df = doc.document_as_df
#     toc = StandardTableOfContent(root_node_name = "root", index_checker = reference_checker, regulation_df = df)


#     sac.tree(items=[
#         sac.TreeItem(doc.document_name, children=[
#             sac.TreeItem(node.get_name()),
#             sac.TreeItem(node.get_name(), children=[
#                 sac.TreeItem(node.get_name()),
#                 sac.TreeItem(node.get_name()),
#                 sac.TreeItem(node.get_name()),
#             ]),
#         ]),
#         sac.TreeItem('disabled', disabled=True),
#         sac.TreeItem('item3', children=[
#             sac.TreeItem('item3-1'),
#             sac.TreeItem('item3-2'),
#         ]),
#     ], label='GDPR Documents', index=0, format_func='title', size='md', icon='table', checkbox=True, checkbox_strict=True)