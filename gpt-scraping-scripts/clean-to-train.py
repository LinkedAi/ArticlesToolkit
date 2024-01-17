"""
OpenCV Documentation Text Cleaning and Merging Script

This script performs two main functions:
1. Cleans text files containing OpenCV documentation by removing extra whitespace, HTML tags, special/control characters, and multiple line breaks.
2. Merges multiple text files from a specified directory into a single output file.

Each text file is processed to ensure it contains clean, readable text, which is then aggregated into one comprehensive document. This is particularly useful for creating datasets or consolidated documents from scattered text files.
"""

import os
import re

# Function to clean text by removing unwanted characters and formatting
def clean_text(text):
    print("Starting text cleaning...")
    # Remove extra white spaces
    text = re.sub(r'\s+', ' ', text).strip()
    print("Extra white spaces removed.")
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    print("HTML tags removed.")
    # Remove special or control characters
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    print("Special or control characters removed.")
    # Reduce multiple line breaks to a single one
    text = re.sub(r'\n+', '\n', text)
    print("Multiple line breaks reduced to a single one.")
    return text

# Function to merge text files from a directory into a single output file
def merge_files(directory, output_file_name):
    print(f"Merging files in the directory '{directory}'...")
    files = [file for file in os.listdir(directory) if file.endswith('.txt')]

    with open(output_file_name, 'w', encoding='utf-8') as output_file:
        for file in files:
            print(f"Processing file: {file}...")
            with open(os.path.join(directory, file), 'r', encoding='utf-8') as input_file:
                content = input_file.read()
                cleaned_content = clean_text(content)
                output_file.write(cleaned_content + '\n\n')
            print(f"File {file} processed and added to the output file.")
    print(f"All files have been merged and saved in '{output_file_name}'.")

# Set the directory and output file name
directory = 'opencv_docs/3.4.x/v1'  # Change this to your folder path with txt files
output_file_name = 'opencv_docs/opencv_dataset_3_4_x.txt'

merge_files(directory, output_file_name)
