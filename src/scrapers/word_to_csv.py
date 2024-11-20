import os
import pandas as pd
from docx import Document  # Library to process DOCX files
from pathlib import Path


CURR_DIRECTORY = Path(__file__).parent

# Define a function to simulate the LexisNexis data reading
def lnt_read(docx_file):
    """
    Simulates the functionality of lnt_read to extract metadata, articles, and paragraphs.
    In reality, you would need to adapt this function for the structure of your DOCX files.
    """
    # Open the DOCX file
    doc = Document(docx_file)
    
    # Example: Extract text and simulate metadata, articles, and paragraphs
    paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
    articles = [{"article_id": i + 1, "content": para} for i, para in enumerate(paragraphs)]
    meta = {"file_name": os.path.basename(docx_file), "num_paragraphs": len(paragraphs)}
    
    # Return structured data
    return {
        "meta": pd.DataFrame([meta]),
        "articles": pd.DataFrame(articles),
        "paragraphs": pd.DataFrame({"paragraphs": paragraphs}),
    }

# Define the main directory
main_dir = f"{CURR_DIRECTORY}/Downloads"

# Get a list of all subdirectories
subfolders = [os.path.join(main_dir, d) for d in os.listdir(main_dir) if os.path.isdir(os.path.join(main_dir, d))]

# Loop through each subfolder
for subfolder in subfolders:
    # Find all DOCX files in the subfolder
    docx_files = [os.path.join(subfolder, f) for f in os.listdir(subfolder) if f.endswith(".DOCX")]
    
    if docx_files:
        # Process the first DOCX file found
        docx_file = docx_files[0]
        
        # Read the LexisNexis document
        LNToutput = lnt_read(docx_file)
        
        # Extract metadata and articles
        meta_df = LNToutput["meta"]
        articles_df = LNToutput["articles"]
        paragraphs_df = LNToutput["paragraphs"]
        
        # Print subfolder name and dimensions of the articles dataframe
        print(f"Processing subfolder: {subfolder}")
        print(f"Articles DataFrame dimensions: {articles_df.shape}")
        
        # Combine metadata and articles (if necessary)
        meta_articles_df = pd.concat([meta_df, articles_df], axis=1)
        
        # Define the output CSV file name
        subfolder_name = os.path.basename(subfolder)
        output_csv = f"{subfolder_name}_meta_articles.csv"
        
        # Write the data to a CSV file
        output_path = os.path.join(subfolder, output_csv)
        meta_articles_df.to_csv(output_path, index=False)
        
        print(f"Data saved to {output_path}")
    else:
        # If no DOCX file is found
        print(f"No DOCX file found in {subfolder}")
