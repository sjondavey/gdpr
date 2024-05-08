import logger
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)
# Create custom log levels for the really detailed logs
DEV_LEVEL = 15
ANALYSIS_LEVEL = 25
logging.addLevelName(DEV_LEVEL, 'DEV')       
logging.addLevelName(ANALYSIS_LEVEL, 'ANALYSIS')       


class Instruction(ABC):
    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def get_description(self):
        pass

    @abstractmethod
    def has_been_followed(self, str):
        pass

class Answer(Instruction):
    def get_name(self):
        return "ANSWER:"

    def get_description(self):
        return f"Answer the question. Preface an answer with the tag '{self.get_name()}'. End the answer with 'Reference: ' and a comma separated list of the extract numbers that you used to answer the question if you used any. Do not include the word Extract in the references section, only provide the number(s)."

    def has_been_followed(self, raw_response):
        
        if not raw_response.startswith(self.get_name()):
            return False

        answer = raw_response[len(self.get_name()):].strip()

        # Extract and clean references from the raw response
        references = answer.split("Reference:")[1].split(",") if "Reference:" in answer else []
        cleaned_references = [ref.strip() for ref in references if ref.strip()]

        # Did not supply any references which is in line with the Instruction
        if not cleaned_references:
            return True

        # Loop through each item in the list
        for item in cleaned_references:
            try:
                # Attempt to convert the item to an integer
                integer_value = int(item)
            except ValueError:
                match = re.search(r'\d', item)
                if not match:
                    return False
        
        return True

    def reformat_response_and_update_search(self, raw_response, df_definitions, df_search_sections):
        # remove the prefix
        raw_response = raw_response[len(self.get_name()):].strip()

        # Extract and clean references from the raw response
        references = raw_response.split("Reference:")[1].split(",") if "Reference:" in raw_response else []
        cleaned_references = [ref.strip() for ref in references if ref.strip()]

        # Early return if no references found
        if not cleaned_references:
            #return [], raw_response.split("Reference:")[0].strip()
            return raw_response, df_definitions, df_search_sections

        integer_references = []
        non_integer_references = []

        # Loop through each item in the list
        for item in cleaned_references:
            try:
                # Attempt to convert the item to an integer
                integer_value = int(item)
                integer_references.append(integer_value)
            except ValueError:
                logger.log(ANALYSIS_LEVEL, f"There are non-integer references: {non_integer_references}")
                # If conversion fails, append to the non_integers list
                non_integer_references.append(item)                
                # Use regular expression to find the first occurrence of a single digit
                match = re.search(r'\d', item)
                if match:
                    integer_references.append(int(match.group(0)))
                    logger.log(ANALYSIS_LEVEL, f" - but the single digit integer {int(match.group(0))} was extracted using re")
                else:
                    logger.error(f"There are non-integer references: {non_integer_references}")
                    return raw_response, df_definitions, df_search_sections
