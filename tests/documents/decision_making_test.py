from gdpr_rag.documents.decision_making import DecisionMaking

import sys
sys.path.append('E:/Code/chat/gdpr')


def test_regression():
    path_to_manual_as_csv_file = "./inputs/documents/decision_making.parquet"

    doc = DecisionMaking(path_to_manual_as_csv_file)
    section = "III.B.6"
    assert doc.get_heading(section) == 'III General provisions on profiling and automated decision-making\nIII.B Lawful bases for processing\nIII.B.6 Article 6(1) (f) - necessary for the legitimate interests[^18] pursued by the controller or by a third party'
    assert doc.get_text(section, add_markdown_decorators = False) == 'III General provisions on profiling and automated decision-making\nIII.B Lawful bases for processing\nIII.B.6 Article 6(1) (f) - necessary for the legitimate interests[^18] pursued by the controller or by a third party\nProfiling is allowed if it is necessary for the purposes of the legitimate interests[^19] pursued by the controller or by a third party. However, Article 6(1) (f) does not automatically apply just because the controller or third party has a legitimate interest. The controller must carry out a balancing exercise to assess whether their interests are overridden by the data subject\'s interests or fundamental rights and freedoms.\nThe following are particularly relevant:\n- the level of detail of the profile (a data subject profiled within a broadly described cohort such as \'people with an interest in English literature\', or segmented and targeted on a granular level);\n- the comprehensiveness of the profile (whether the profile only describes a small aspect of the data subject, or paints a more comprehensive picture);\n- the impact of the profiling (the effects on the data subject); and\n- the safeguards aimed at ensuring fairness, non-discrimination and accuracy in the profiling process.\nAlthough the WP29 opinion on legitimate interests[^20] is based on Article 7 of the data protection Directive 95/46/EC (the Directive), it contains examples that are still useful and relevant for controllers carrying out profiling. It also suggests it would be difficult for controllers to justify using legitimate interests as a lawful basis for intrusive profiling and tracking practices for marketing or advertising purposes, for example those that involve tracking individuals across multiple websites, locations, devices, services or  data-brokering.\nThe controller should also consider the future use or combination of profiles when assessing the validity of processing under Article 6(1) (f).\n\n  \n[^18]: Legitimate interests listed in GDPR Recital 47 include processing for direct marketing purposes and processing strictly necessary for the purposes of preventing fraud.  \n[^19]: The controller\'s "legitimate interest" cannot render profiling lawful if the processing falls within the Article 22(1) definition.  \n[^20]: Article 29 Data Protection Working Party. Opinion 06/2014 on the notion of legitimate interests of the data controller under Article 7 of Directive 95/46/EC. European Commission, 9 April 2014, Page 47, examples on pages 59 and 60 http://ec.europa.eu/justice/data-protection/article-29/documentation/opinion- recommendation/files/2014/wp217_en.pdf . Accessed 24 April 2017'


    section = 'Annex 1'
    assert doc.get_heading(section) == 'Annex 1 Good practice recommendations'
    assert doc.get_text(section, add_markdown_decorators = False) == "Annex 1 Good practice recommendations\nThe following good practice recommendations will assist data controllers in meeting the requirements of the GDPR provisions on profiling and automated decision making.[^52]\n|Article |Issue |Recommendation |\n|---|---|---|\n|5(1)(a),12, 13, 14 | Right to have information | Controllers should consult the WP29 Guidelines on transparency WP260 for general transparency requirements. In addition to the general requirements, when the controller is processing data as defined in Article 22, they must provide meaningful information about the logic involved. Instead of providing a complex mathematical explanation about how algorithms or machine-learning work, the controller should consider using clear and comprehensive ways to deliver the information to the data subject, for example: <li> the categories of data that have been or will be used in the profiling or decision-making process </li><li> why these categories are considered pertinent </li><li> how any profile used in the automated decision-making process is built, including any statistics used in the analysis </li><li> why this profile is relevant to the automated decision-making process; and </li><li> how it is used for a decision concerning the data subject. </li>Such information will generally be more relevant to the data subject and contribute to the transparency of the processing. <br> Controllers may wish to consider visualisation and interactive techniques to aid algorithmic transparency[^53]. |\n|6(1)(a) |Consent as a basis for processing | If controllers are relying upon consent as a basis for processing they should consult the WP29 Guidelines on consent WP259. |\n|15 | Right of access | Controllers may want to consider implementing a mechanism for data subjects to check their profile, including details of the information and sources used to develop it. |\n|16 | Right to rectification | Controllers providing data subjects with access to their profile in connection with their Article 15 rights should allow them the opportunity to update or amend any inaccuracies in the data or profile. <br> This can also help them meet their Article 5(1) (d) obligations. Controllers could consider introducing online preference management tools such as a privacy dashboard. This gives data subjects the option of managing what is happening to their information across a number of different services - allowing them to alter settings, update their personal details, and review or edit their profile to correct any inaccuracies. |\n|21(1) and (2) | Right to object | The right to object in Article 21(1) and (2) has to be explicitly brought to the attention of the data subject and presented clearly and separately from other information (Article 21(4). <br> Controllers need to ensure that this right is prominently displayed on their website or in any relevant documentation and not hidden away within any other terms and conditions. |\n|22 and Recital 71 | Appropriate safeguards | The following list, though not exhaustive, provides some good practice suggestions for controllers to consider when making solely automated decisions, including profiling(defined in Article 22(1)): <li> regular quality assurance checks of their systems to make sure that individuals are being treated fairly and not discriminated against, whether on the basis of special categories of personal data or otherwise; </li><li> algorithmic auditing - testing the algorithms used and developed by machine learning systems to prove that they are actually performing as intended, and not producing discriminatory, erroneous or unjustified results; </li><li> for independent 'third party' auditing (where decision-making based on profiling has a high impact on individuals), provide the auditor with all necessary information about how the algorithm or machine learning system works; </li><li> obtaining contractual assurances for third party algorithms that auditing and testing has been carried out and the algorithm is compliant with agreed standards; </li><li> specific measures for data minimisation to incorporate clear retention periods for profiles and for any personal data used when creating or applying the profiles; </li><li> using anonymisation or pseudonymisation techniques in the context of profiling; </li><li> ways to allow the data subject to express his or her point of view and contest the decision; and, </li><li> a mechanism for human intervention in defined cases, for example  providing a link to an appeals process at the point the automated decision is delivered to the data subject, with agreed timescales for the  review and a named contact point for any queries.</li> <br> Controllers can also explore options such as: <li> certification mechanisms for processing operations; </li><li> codes of conduct for auditing processes involving machine learning; </li><li> ethical review boards to assess the potential harms and benefits to society of particular applications for profiling. |\n\n  \n[^52]: Controllers also need to ensure they have robust procedures in place to ensure that they can meet their obligations under Articles 15 - 22 in the timescales provided for by the GDPR.  \n[^53]: Information Commissioner's Office - Big data, artificial intelligence, machine learning and data protection version 2.0, 03/2017. Page 87, paragraph 194, March 2017. https://ico.org.uk/media/for- organisations/documents/2013559/big-data-ai-ml-and-data-protection.pdf  Accessed 24 April 2017"

    
    # Special case for section IV
    section = "IV"
    assert doc.get_heading(section) == 'IV Specific provisions on solely automated decision- making as defined in Article 22'
    assert doc.get_text(section, add_markdown_decorators = False) == 'IV Specific provisions on solely automated decision- making as defined in Article 22\nArticle 22(1) says\n"The data subject shall have the right not to be subject to a decision based solely on automated processing, including profiling, which produces legal effects concerning him or her or similarly significantly affects him or her."\nThe term "right" in the provision does not mean that Article 22(1) applies only when actively invoked by the data subject. Article 22(1) establishes a general prohibition for decision-making based solely on automated processing. This prohibition applies whether or not the data subject takes an action regarding the processing of their personal data.\nIn summary, Article 22 provides that:\n(i) as a rule, there is a general prohibition on fully automated individual decision-making, including profiling that has a legal or similarly significant effect;\n(ii) there are exceptions to the rule;\n(iii) where one of these exceptions applies, there must be measures in place to safeguard the data subject\'s rights and freedoms and legitimate interests[^32].\nThis interpretation reinforces the idea of the data subject having control over their personal data, which is in line with the fundamental principles of the GDPR.  Interpreting Article 22 as a prohibition rather than a right to be invoked means that individuals are automatically protected from the potential effects this type of processing may have. The wording of the Article suggests that this is the intention and is supported by Recital 71 which says:\n"However, decision-making based on such processing, including profiling, should be allowed where expressly authorised by Union or Member State law……, or necessary for the entering or performance of a contract……., or when the data subject has given his or her explicit consent"\nThis implies that processing under Article 22(1) is not allowed generally.[^33]\nHowever the Article 22(1) prohibition only applies in specific circumstances when a decision based solely on automated processing, including profiling, has a legal effect on or similarly significantly affects someone, as explained further in the guidelines. Even in these cases there are defined exceptions which allow such processing to take place.\nThe required safeguarding measures, discussed in more detail below, include the right to be informed (addressed in Articles 13 and 14 - specifically meaningful information about the logic involved, as well as the significance and envisaged consequences for the data subject), and safeguards, such as the right to obtain human intervention and the right to challenge the decision (addressed in Article 22(3)).\nAny processing likely to result in a high risk to data subjects requires the controller to carry out a Data Protection Impact Assessment (DPIA).[^34] As well as addressing any other risks connected with the processing, a DPIA can be particularly useful for controllers who are unsure whether their proposed activities will fall within the Article 22(1) definition, and, if allowed by an identified exception, what safeguarding measures must be applied.\n\n  \n[^32]: Recital 71 says that such processing should be "subject to suitable safeguards, which should include specific information to the data subject and the right to obtain human intervention, to express his or her point of view, to obtain an explanation of the decision reached after such assessment and to challenge the decision."  \n[^33]: Further comments on the interpretation of Article 22 as a prohibition can be found in Annex 2.  \n[^34]: Article 29 Data Protection Working Party. Guidelines on Data Protection Impact Assessment (DPIA) and determining whether processing is "likely to result in a high risk" for the purposes of Regulation 2016/679. 4 April 2017. European Commission. http://ec.europa.eu/newsroom/document.cfm?doc_id=44137 Accessed 24 April 2017.'


    section = "IV.E"
    assert doc.get_heading(section) == 'IV Specific provisions on solely automated decision- making as defined in Article 22\nIV.E Rights of the data subject[^37]'
    assert doc.get_text(section, add_markdown_decorators = False) == "IV Specific provisions on solely automated decision- making as defined in Article 22\nIV.E Rights of the data subject[^37]\n\n  \n[^37]: GDPR Article 12 provides for the modalities applicable for the exercise of the data subject's rights"

    
    
    section = "IV.E.1"
    assert doc.get_heading(section) == 'IV Specific provisions on solely automated decision- making as defined in Article 22\nIV.E Rights of the data subject[^37]\nIV.E.1 Articles 13(2) (f) and 14(2) (g) - Right to be informed'
    assert doc.get_text(section, add_markdown_decorators = False) == 'IV Specific provisions on solely automated decision- making as defined in Article 22\nIV.E Rights of the data subject[^37]\nIV.E.1 Articles 13(2) (f) and 14(2) (g) - Right to be informed\nGiven the potential risks and interference that profiling caught by Article 22 poses to the rights of data subjects, data controllers should be particularly mindful of their transparency obligations.\nArticles 13(2) (f) and 14(2) (g) require controllers to provide specific, easily accessible information about automated decision-making, based solely on automated processing, including profiling, that produces legal or similarly significant effects.[^38]\nIf the controller is making automated decisions as described in Article 22(1), they must:\n- tell the data subject that they are engaging in this type of activity;\n- provide meaningful information about the logic involved; and\n- explain the significance and envisaged consequences of the processing.\nProviding this information will also help controllers ensure they are meeting some of the required safeguards referred to in Article 22(3) and Recital 71.\nIf the automated decision-making and profiling does not meet the Article 22(1) definition it is nevertheless good practice to provide the above information. In any event the controller must provide sufficient information to the data subject to make the processing fair,[^39] and meet all the other information requirements of Articles 13 and 14.\nMeaningful information about the \'logic involved\'\nThe growth and complexity of machine-learning can make it challenging to understand how an automated decision-making process or profiling works.\nThe controller should find simple ways to tell the data subject about the rationale behind, or the criteria relied on in reaching the decision. The GDPR requires the controller to provide meaningful information about the logic involved, not necessarily a complex explanation of the algorithms used or disclosure of the full algorithm.[^40]  The information provided should, however, be sufficiently comprehensive for the data subject to understand the reasons for the decision.\nExample\nA controller uses credit scoring to assess and reject an individual\'s loan application. The score may have been provided by a credit reference agency, or calculated directly based on information held by the controller.<br>Regardless of the source (and information on the source must be provided to the data subject under Article 14 (2) (f) where the personal data have not been obtained from the data subject), if the controller is reliant upon this score it must be able to explain it and the rationale, to the data subject.<br>The controller explains that this process helps them make fair and responsible lending decisions. It provides details of the main characteristics considered in reaching the decision, the source of this information and the relevance. This may include, for example:<br><li> the information provided by the data subject on the application form;</li><li> information about previous account conduct , including any payment arrears; and </li><li> official public records information such as fraud record information and insolvency records.</li> <br> The controller also includes information to advise the data subject that the credit scoring methods used are regularly tested to ensure they remain fair, effective and unbiased. The controller provides contact details for the data subject to request that any declined decision is reconsidered, in line with the provisions of Article 22(3).\n\'Significance\' and \'envisaged consequences\'\nThis term suggests that information must be provided about intended or future processing, and how the automated decision-making might affect the data subject.[^41] In order to make this information meaningful and understandable, real, tangible examples of the type of possible effects should be given. In a digital context, controllers might be able to use additional tools to help illustrate such effects.\nExample\nAn insurance company uses an automated decision making process to set motor insurance premiums based on monitoring customers\' driving behaviour. To illustrate the significance and envisaged consequences of the processing it explains that dangerous driving may result in higher insurance payments and provides an app comparing fictional drivers, including one with dangerous driving habits such as fast acceleration and last-minute braking. <br>It uses graphics to give tips on how to improve these habits and consequently how to lower insurance premiums.\nControllers can use similar visual techniques to explain how a past decision has been made.\n\n  \n[^37]: GDPR Article 12 provides for the modalities applicable for the exercise of the data subject\'s rights  \n[^38]: Referred to in Article 22(1) and (4).The WP Guidelines on transparency cover the general information requirements set out in Articles 13 and 14.  \n[^39]: GDPR Recital 60 "The controller should provide the data subject with any further information necessary to ensure fair and transparent processing taking into account the specific circumstances and context in which th e personal data are processed. Furthermore the data subject should be informed of the existence of profiling and the consequences of such profiling."  \n[^40]: Complexity is no excuse for failing to provide information to the data subject. Recital 58 states that the principle of transparency is "of particular relevance in situations where the proliferation of actors and the technological complexity of practice makes it difficult for the data subject to know and understand whether, by whom and for what purpose personal data relating to him are being collected, such as in the case of online advertising".  \n[^41]: Council of Europe. Draft Explanatory Report on the modernised version of CoE Convention 108, paragraph 75: "Data subjects should be entitled to know the reasoning underlying the processing of their data, including the consequences of such a reasoning, which led to any resulting conclusions, in particular in cases involving the use of algorithms for automated-decision making including profiling. For instance in the case of credit scoring, they should be entitled to know the logic underpinning the processing of their data and resulting in a \'yes\' or \'no\' decision, and not simply information on the decision itself. Without an understanding of these elements there could be no effective exercise of other essential safeguards such as the right to object and the right to complain to a competent authority." https://rm.coe.int/CoERMPublicCommonSearchServices/DisplayDCTMContent?documentId=09000016806b6e c2 . Accessed 24 April 2017'

    