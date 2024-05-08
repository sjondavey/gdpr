import re
import fitz


def output_doc_as_text(pdf_doc, start_page = 0, end_page = 0, header_size=80, footer_size=40, lines_to_delete = [], characters_to_replace = []):
    if end_page == 0 or end_page > len(pdf_doc):
        end_page = len(pdf_doc)
    if end_page < start_page:
        print("End page before start page! Doing nothing")
    combined_text = ''
    for page_number in range(start_page, end_page):
        page = pdf_doc[page_number]
        tl = page.rect[0], page.rect[1]  # lower-left coordinates
        br = page.rect[2], page.rect[3]  # upper-right
        rect = fitz.Rect(tl[0], tl[1]+header_size, br[0], br[1]-footer_size)
        raw_text = page.get_text('text', clip=rect)

        cleaned_text = clean_text(raw_text, lines_to_delete=lines_to_delete, characters_to_replace=characters_to_replace)
        combined_text += cleaned_text
    return combined_text


def clean_text(text, lines_to_delete, characters_to_replace):
    '''
        lines_to_replace: a list of lines to delete. Some documents have page or section ends like "---oOo---"
        characters_to_replace: a list of lists. The first item in the list is the text to replace, the second is the replacement text
    '''
    lines = text.split("\n")
    cleaned_lines = []
    for line in lines:
        if line.strip():  # If the line contains text other than whitespace
            line_text = line.strip()
            if line_text not in lines_to_delete:
                cleaned_lines.append(line_text)
        else:  # If the line is blank
            if cleaned_lines and cleaned_lines[-1] != "\n":  
                cleaned_lines.append("\n")
    cleaned_text = " ".join(cleaned_lines).replace(" \n ", "\n")
    for replacement in characters_to_replace:
        cleaned_text = cleaned_text.replace(replacement[0], replacement[1])
    
    return cleaned_text

    #return " ".join(cleaned_lines)
    
