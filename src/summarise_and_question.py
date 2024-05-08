# Update the relevant summary row
import openai

system_content = "You are summarising Articles from the General Data Protection Regulation (GDPR) from the perspective of a controller. When summarising, do not add filler words like 'GDPR says ...', or 'Article x says ...', just provide the summary without any explanation. Where possible replace defined terms like 'data subject' with 'individual' or 'controller' with 'you' (i.e. with less formal terms instead of definitions). Pay special attention to any mandatory actions - where and when these need to happen and who is responsible for them. Please use UK English."



system_content_question = "You helping to prepare a set of Frequently Asked Questions (FAQs) for the Article from the General Data Protection Regulation (GDPR) provided for a controller. The questions should be high level to cover the different themes in the answer. Where possible replace defined terms like 'data subject' with 'individual' or 'controller' with 'you' (i.e. with less formal terms instead of definitions). The questions should not focus on details like 'Which Article says ...'. They also should try to avoid statements like 'According to GDPR' because that context can be taken for granted. When creating questions, please use acronyms but also provide the expanded version of the acronym in every question because they will be used separately so all context needs to be available in each. \n\
List your questions as a pipe delimited string. Please use UK English. Below are examples to guide you. \n\
#### Example 1 Input\n\
Article 1 Subject-matter and objectives\n\
    1. This Regulation lays down rules relating to the protection of natural persons with regard to the processing of personal data and rules relating to the free movement of personal data.\n\
    2. This Regulation protects fundamental rights and freedoms of natural persons and in particular their right to the protection of personal data.\n\
    3. The free movement of personal data within the Union shall be neither restricted nor prohibited for reasons connected with the protection of natural persons with regard to the processing of personal data.\n\
#### Example 1 Questions\n\
What are the objectives of General Data Protection Regulation (GDPR)?|What is covered in General Data Protection Regulation (GDPR)?|Who does General Data Protection Regulation (GDPR) protect?|Does General Data Protection Regulation (GDPR) prevent personal data from being moved or processed elsewhere in the European Union?\n\
#### Example 2 Input\n\
Article 70 Tasks of the Board\n\
    1. The Board shall ensure the consistent application of this Regulation. To that end, the Board shall, on its own initiative or, where relevant, at the request of the Commission, in particular:\n\
        (e) examine, on its own initiative, on request of one of its members or on request of the Commission, any question covering the application of this Regulation and issue guidelines, recommendations and best practices in order to encourage consistent application of this Regulation;\n\
        (f) issue guidelines, recommendations and best practices in accordance with point (e) of this paragraph for further specifying the criteria and conditions for decisions based on profiling pursuant to Article 22(2);\n\
        (g) issue guidelines, recommendations and best practices in accordance with point (e) of this paragraph for establishing the personal data breaches and determining the undue delay referred to in Article 33(1) and (2) and for the particular circumstances in which a controller or a processor is required to notify the personal data breach;\n\
        (h) issue guidelines, recommendations and best practices in accordance with point (e) of this paragraph as to the circumstances in which a personal data breach is likely to result in a high risk to the rights and freedoms of the natural persons referred to in Article 34(1).\n\
#### Example 2 Question\n\
Who insures the regulations are consistently applied?|How is consistency achieved?|Who determines best practice?|Who decided when profiling is allowed?Who decides on the best practices for managing a data breach?"



def get_summary_and_questions_for(openai_client, text, model):
    user_content = text
    response = openai_client.chat.completions.create(
                        model=model,
                        temperature = 1.0,
                        max_tokens = 500,
                        messages=[
                            {"role": "system", "content": system_content},
                            {"role": "user", "content": user_content},
                        ]
                    )
    summary = response.choices[0].message.content


    user_content_question = text
    response = openai_client.chat.completions.create(
                        model=model,
                        temperature = 1.0,
                        max_tokens = 500,
                        messages=[
                            {"role": "system", "content": system_content_question},
                            {"role": "user", "content": user_content_question},
                        ]
                    )
    questions = response.choices[0].message.content

    return summary, questions

