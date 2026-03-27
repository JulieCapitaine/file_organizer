# Exercise: File Organizer & Cleaner

## Objective
Build a Python script that organizes files, cleans .txt files, and generates a complete report.

## Context
You receive a folder inbox/ filled with files of various types:
- .txt
- .log
- .csv
- .json
- .png / .jpg
- etc.

You must write a Python script that:
- Never modifies the source folder
- Sorts files into an output/ folder by their extension
- Cleans .txt files (see below)
- Logs all operations to the console
- Produces a final report (statistics)

---

## Instructions:
- Follow the steps in order.
- Write clean, modular, and well-commented code.
- Make sure your script is robust and handles errors gracefully.
- Test your script with given inbox folder.

---

## Step 1: Run main
```
python main.py --source inbox
```

## Step 2: Create the Destination Folder
Create the destination folder. If it already exists, empty its contents.

Example usage:
```
python main.py --source inbox --destination output
```

## Step 3: Sort Files by Type

In the destination folder, create 4 subfolders to sort files by extension:
- images: .jpg, .jpeg, .png
- docs: .pdf, .doc, .docx, .txt, .md, .log
- data: .csv, .json, .xml
- others: all other extensions

For each file found in the source folder, copy (do not move!) the file into the appropriate subfolder in the destination.  
Your script must be able to map any file extension to the correct category.

## Step 4: Clean .txt Files
If the --clean option is enabled, clean all .txt files by:
- Removing empty lines
- Removing leading and trailing spaces from each line

Example usage:
```
python main.py --source inbox --destination output -- clean
```

## Step 5: Generate a Report
At the end of the script, create a file report_DATE.txt in the destination folder containing:
- Total number of files processed
- Number of files per type (images, docs, data, others)
- List of cleaned .txt files (if --clean is enabled)

Use the current date (YYYY-MM-DD) for the DATE part of the report filename.
