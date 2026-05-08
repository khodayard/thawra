import os
import re

# Set up your folder names
INPUT_DIR = 'raw_podcasts'
ENG_OUT_DIR = 'english_books'
PER_OUT_DIR = 'persian_books'

# Create the output directories if they do not exist
os.makedirs(ENG_OUT_DIR, exist_ok=True)
os.makedirs(PER_OUT_DIR, exist_ok=True)

def is_persian(text):
    # Checks if the text contains characters in the Persian/Arabic Unicode range
    return bool(re.search(r'[\u0600-\u06FF]', text))

def process_files():
    # Loop through every text file in the raw folder
    for filename in os.listdir(INPUT_DIR):
        if not filename.endswith('.txt'):
            continue
            
        filepath = os.path.join(INPUT_DIR, filename)
        
        english_content = []
        persian_content = []
        
        with open(filepath, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            
        for line in lines:
            clean_line = line.strip()
            
            # Preserve intentional paragraph breaks
            if not clean_line:
                english_content.append('\n')
                persian_content.append('\n')
                continue
                
            # Route to the correct array based on Unicode characters
            if is_persian(clean_line):
                persian_content.append(clean_line + '\n\n')
            else:
                english_content.append(clean_line + '\n\n')
                
        # Save the separated files into their respective folders
        eng_output_path = os.path.join(ENG_OUT_DIR, f'ENG_{filename}')
        per_output_path = os.path.join(PER_OUT_DIR, f'PER_{filename}')
        
        with open(eng_output_path, 'w', encoding='utf-8') as eng_file:
            eng_file.writelines(english_content)
            
        with open(per_output_path, 'w', encoding='utf-8') as per_file:
            per_file.writelines(persian_content)
            
        print(f"Success: Separated {filename}")

if __name__ == '__main__':
    print("Starting the language separation...")
    process_files()
    print("Complete. Your files are ready in the english_books and persian_books folders.")