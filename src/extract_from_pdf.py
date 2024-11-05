import re
import string
import fitz


# For ICO "html to pdf" documents. This provides the base text extraction from the pdf.
# NOTE: It is far from perfect
def extract_text_sorted_with_links(pdf_path, header_size=20, footer_size=50, paragraph_gap_threshold=5):
    # Open the PDF file
    document = fitz.open(pdf_path)
    
    all_text = []
    
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        
        # Get the page height
        page_height = page.rect.height
        
        # Get all text blocks
        blocks = page.get_text('blocks')
        
        # Get all links on the page
        links = page.get_links()
        
        # Filter out blocks that fall within the header or footer area
        filtered_blocks = [
            block for block in blocks
            if block[1] > header_size and block[3] < (page_height - footer_size)
        ]
        
        # Sort blocks by vertical position (y0 value)
        blocks_sorted = sorted(filtered_blocks, key=lambda b: b[1])  # b[1] is y0
        
        # Create a dictionary to store links by their position
        link_dict = {}
        for link in links:
            if 'uri' in link:  # External link
                link_dict[(link['from'][0], link['from'][1], link['from'][2], link['from'][3])] = ('external', link['uri'])
            elif 'xref' in link:  # Internal link
                target_page = link['xref']
                link_dict[(link['from'][0], link['from'][1], link['from'][2], link['from'][3])] = ('internal', target_page)
        
        # Combine text from sorted blocks and preserve links in markdown format
        page_text = ""
        prev_block_bottom = None
        for block in blocks_sorted:
            block_text = block[4].strip()  # block[4] is the text
            if block_text:
                # Check if there is a significant vertical gap between blocks (indicating a paragraph break)
                if prev_block_bottom is not None and (block[1] - prev_block_bottom) > paragraph_gap_threshold:
                    page_text += "\n\n"  # Add paragraph break
                
                # Check if this block has a link
                for (x0, y0, x1, y1), (link_type, target) in link_dict.items():
                    if x0 <= block[0] <= x1 and y0 <= block[1] <= y1:
                        if link_type == 'external':
                            block_text = f"[{block_text}]({target})"
                        elif link_type == 'internal':
                            block_text = f"[{block_text}](#page-{target})"
                        break
                
                page_text += block_text + "\n"
                prev_block_bottom = block[3]  # Update the bottom of the current block
        
        all_text.append(page_text)
    
    # Close the document
    document.close()
    
    return "\n".join(all_text)


def process_markdown_links(text):
    # Regex to match the markdown internal links
    pattern = re.compile(r'\[([^\]]+)\]\(#page-\d{1,3}\)')
    
    # List to store all instances of link_text where changes were made
    modified_links = []
    
    def replace_link(match):
        link_text = match.group(1)
        # Create the reformatted version of link_text
        reformatted_text = re.sub(r'[^\w\s]', '', link_text).lower().replace(' ', '-')
        modified_links.append(link_text)
        return f'[{link_text}](#{reformatted_text})'
    
    # Replace the link_page with the reformatted link_text
    new_text = re.sub(pattern, replace_link, text)
    
    return new_text, modified_links
    

def replace_link_headers(new_text, modified_links):
    lines = new_text.splitlines()
    
    for link in modified_links:
        # Find all occurrences of the link that start a new line
        matches = [i for i, line in enumerate(lines) if line.strip().startswith(link)]
        
        # Replace the line with "## link" if there is only one match
        if len(matches) == 1:
            lines[matches[0]] = f"## {link}"
    
    # Join the lines back into a single string
    updated_text = "\n".join(lines)
    
    return updated_text


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
        
        # raw_text = page.get_text('text', clip=rect)
        # cleaned_text = clean_text(raw_text, lines_to_delete=lines_to_delete, characters_to_replace=characters_to_replace)
        
        raw_text = page.get_text('blocks', clip=rect)
        cleaned_text = clean_blocks(raw_text, lines_to_delete=lines_to_delete, characters_to_replace=characters_to_replace)

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
    

def clean_blocks(blocks, lines_to_delete, characters_to_replace):
    page_text = ""
    for block in blocks:
            if block[6] == 0:  # block type: text
                block_text = block[4]
                block_text = block_text.replace("\n", " ")  # Replace newlines within paragraphs

                page_text += block_text + "\n"  # Add newline to separate paragraphs

    for replacement in characters_to_replace:
        page_text = page_text.replace(replacement[0], replacement[1])
    for replacement in lines_to_delete:
        page_text = page_text.replace(replacement, "")
    return page_text
