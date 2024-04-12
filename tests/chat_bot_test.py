# import pandas as pd
# from openai import OpenAI
# import os

# import importlib
# import src.chat_bot
# importlib.reload(src.chat_bot)
# from src.chat_bot import QuestionAnswering

# import importlib
# import src.data
# importlib.reload(src.data)
# from src.data import load_parquet_data, load_gdpr_data_from_folders, EmbeddingParameters, load_embedding_parameters, ChatParameters, load_chat_parameters


# class TestGDPR:
#     openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"),)
#     embedding_parameters = EmbeddingParameters(embedding_model = "text-embedding-3-large", embedding_dimensions = 1024)
#     chat_parameters = ChatParameters(chat_model = "gpt-3.5-turbo", temperature = 0, max_tokens = 500)
#     data = load_gdpr_data_from_folders(base_directory = "./inputs")

#     gdpr = QuestionAnswering(openai_client = openai_client, 
#                              embedding_parameters = embedding_parameters,
#                              chat_parameters = chat_parameters,
#                              data = data)

#     def test_construction(self):
#         assert True

#     def test__add_rag_data_to_question(self):
#         question = "What is GDPR?"
#         definitions = [] 
#         references = []
#         rag_question = self.gdpr._add_rag_data_to_question(question, definitions, references)
#         assert rag_question == "Question: " + question

#         definitions = ["GDPR is a set of laws", "GDPR applies in Europe"] 
#         rag_question = self.gdpr._add_rag_data_to_question(question, definitions, references)
#         assert rag_question == f"Question: {question}\nDefinitions\n{definitions[0]}\n{definitions[1]}"

#         references = ["The regs", "Wikipedia"]
#         rag_question = self.gdpr._add_rag_data_to_question(question, definitions, references)
#         assert rag_question == f"Question: {question}\nDefinitions\n{definitions[0]}\n{definitions[1]}\nReferences\n{references[0]}\n{references[1]}"

#         definitions = []
#         rag_question = self.gdpr._add_rag_data_to_question(question, definitions, references)
#         assert rag_question == f"Question: {question}\nReferences\n{references[0]}\n{references[1]}"

#     def test__extract_question_from_rag_data(self):
#         question = "What is GDPR?" 
#         # return the input if it does not start with "Question:"
#         output = self.gdpr._extract_question_from_rag_data(question)
#         assert output == question

#         input = f"Question: {question}"
#         output = self.gdpr._extract_question_from_rag_data(input)
#         assert output == question

#         input = f"Question: {question}\n"
#         output = self.gdpr._extract_question_from_rag_data(input)
#         assert output == question

#         input = f"Question: {question}\n\n some text here"
#         output = self.gdpr._extract_question_from_rag_data(input)
#         assert output == question

#         input = f"Question: {question} more text but on the same line"
#         output = self.gdpr._extract_question_from_rag_data(input)
#         assert output != question

#     def test_append_content(self):
#         self.gdpr.append_content('user', 'Question: What documents are required')
#         assert len(self.gdpr.messages) == 1
#         assert self.gdpr.messages[-1]['content'] == 'Question: What documents are required'
#         assert self.gdpr.messages[-1]['role'] == 'user'

#         assert len(self.gdpr.messages_without_rag) == 1
#         assert self.gdpr.messages_without_rag[-1]['role'] == 'user'
#         assert self.gdpr.messages_without_rag[-1]['content'] == 'What documents are required'

#         # Try to add content for a role that does not exist
#         self.gdpr.reset_conversation_history()
#         self.gdpr.append_content('other_role', 'Question: What documents are required')
#         assert len(self.gdpr.messages) == 0
#         assert len(self.gdpr.messages_without_rag) == 0

#         self.gdpr.reset_conversation_history()
#         self.gdpr.append_content('assistant', 'Answer here')
#         assert len(self.gdpr.messages) == 1
#         assert self.gdpr.messages[-1]['content'] == 'Answer here'
#         assert self.gdpr.messages[-1]['role'] == 'assistant'

#         assert len(self.gdpr.messages_without_rag) == 1
#         assert self.gdpr.messages_without_rag[-1]['role'] == 'assistant'
#         assert self.gdpr.messages_without_rag[-1]['content'] == 'Answer here'

#     def test_get_regulation_detail_for_section(self):
#         expected_answer = "Article 14 Information to be provided where personal data have not been obtained from the data subject\n    1. Where personal data have not been obtained from the data subject, the controller shall provide the data subject with the following information:\n        (a) the identity and the contact details of the controller and, where applicable, of the controller's representative;\n"
#         retrieved_answer = self.gdpr.get_regulation_detail_for_section("14(1)(a)")
#         assert expected_answer == retrieved_answer

#     def test_get_regulation_detail_for_sections(self):
#         list_of_section_references = ['14(1)(a)', "98"]
#         df_sections = self.gdpr.get_regulation_detail_for_sections(list_of_section_references)
#         assert len(df_sections) == 2
#         expected_answer = 'Article 98 Review of other Union legal acts on data protection\nThe Commission shall, if appropriate, submit legislative proposals with a view to amending other Union legal acts on the protection of personal data, in order to ensure uniform and consistent protection of natural persons with regard to processing. This shall in particular concern the rules relating to the protection of natural persons with regard to processing by Union institutions, bodies, offices and agencies and on the free movement of such data.\n'
#         assert df_sections.iloc[1]['text'] == expected_answer

#     def test__create_system_message(self):
#         expected_answer = "You are answering questions for a controller based on extracts from the General Data Protection Regulation (GDPR) that are provided. Please use the text's index pattern when referring to sections of it: ^Article (\\d{1,2})(?:\\((\\d{1,2})\\))?(?:\\(([a-z])\\))?.\nYou have three options:\n1) Answer the question. Preface an answer with the tag 'ANSWER:'. End the answer with 'Reference: ' and a comma separated list of the indexes you used to answer the question if you used any.\n2) Request additional documentation. If, in the body of the references provided, there is a reference to another section of the document that is directly relevant and not already provided, respond with the word 'INDEX:' followed by the section reference.\n3) State 'NONE:' and nothing else in all other cases"
#         system_content = self.gdpr._create_system_message()
#         assert expected_answer == system_content


#     def test_similarity_search(self):
#         # Check that random chit-chat to the main dataset does not return any hits from the embeddings
#         text = "Hi"
#         workflow_triggered, df_definitions, df_search_sections = self.gdpr.similarity_search(text)
#         assert len(df_definitions) == 0
#         assert len(df_search_sections) == 0 
#         # now move to the testing dataset for fine grained tests
#         user_content = "What is personal data?"
#         workflow_triggered, relevant_definitions, relevant_sections = self.gdpr.similarity_search(user_content)
#         assert workflow_triggered == "none"
#         assert len(relevant_definitions) == 1
#         assert len(relevant_sections) == 3
#         assert relevant_sections.iloc[0]["section"] == '9'
#         assert relevant_sections.iloc[1]["section"] == '5'
#         assert relevant_sections.iloc[2]["section"] == '90'
