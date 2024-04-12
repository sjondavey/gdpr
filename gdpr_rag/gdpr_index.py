from regulations_rag.standard_regulation_index import StandardRegulationIndex, load_index_data_from_files
from regulations_rag.regulation_reader import  load_regulation_data_from_files

from gdpr_rag.gdpr_reference_checker import GDPRReferenceChecker
from gdpr_rag.gdpr_reader import GDPRReader

class GDPRIndex(StandardRegulationIndex):

    def __init__(self, decryption_key):
        user_type = "a Controller"
        regulation_name = "General Data Protection Regulation (GDPR)"


        path_to_manual_as_csv_file = "./inputs/gdpr.csv"
        path_to_additional_manual_as_csv_file = ""
        df_regulations = load_regulation_data_from_files(path_to_manual_as_csv_file, 
                                                         path_to_additional_manual_as_csv_file)

        path_to_definitions_as_parquet_file = "./inputs/definitions_gdpr.parquet"
        path_to_additional_definitions_as_parquet_file = ""
        path_to_index_as_parquet_file = "./inputs/index_gdpr.parquet"
        path_to_additional_index_as_parquet_file = ""
        path_to_workflow_as_parquet = ""

        # decryption_key = os.getenv('excon_encryption_key')
        df_definitions, df_index, df_workflow = load_index_data_from_files(path_to_definitions_as_parquet_file, 
                                                                           path_to_additional_definitions_as_parquet_file, 
                                                                           path_to_index_as_parquet_file, 
                                                                           path_to_additional_index_as_parquet_file, 
                                                                           path_to_workflow_as_parquet, 
                                                                           decryption_key=decryption_key)


        reference_checker = GDPRReferenceChecker()
        reader = GDPRReader()

        super().__init__(user_type = user_type, 
                         regulation_name = regulation_name, 
                         regulation_reader = reader,
                         df_definitions = df_definitions, 
                         df_index = df_index, 
                         df_workflow = df_workflow)

