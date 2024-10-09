https://www.edpb.europa.eu/our-work-tools/general-guidance/guidelines-recommendations-best-practices_en


https://www.edpb.europa.eu/about-edpb/publications/one-stop-shop-case-digests_en
Final One Stop Shop Decisions
https://www.edpb.europa.eu/our-work-tools/consistency-findings/register-for-article-60-final-decisions_en

https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A52020DC0264
https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A52020SC0115

https://ico.org.uk/

## Brain dump

There are lots of documents about GDPR [^1]. I need
1) A place for the original (pdf / web text etc): Folder ./original/
2) A notebook to 
    a) convert the original into a dataframe; folder ./inputs/documents/     
    b) to create summaries and questions that can be added to the document index (QUESTION: is this one file / table or one per document?) ./inputs/
   There notebooks are to be saved in folder ./conversion_notebooks/
3) A document.py wrapper for the dataframe version of the document ./gdpr_rag/documents/
4) A naming convention that that allows a script to check that each original document has been converted into a dataframe, has a document.py wrapper and has been added to the document index. This should also check that there are no additional entries in the document index etc.

[^1]: Here is footnote 1
