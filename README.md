# FEC Data Analysis Tools

This repository contains a set of Python tools designed for analyzing individual contribution data from the official Federal Election Commission (FEC) website. These tools allow you to filter, count, and analyze contribution data based on various parameters.

## Prerequisites

- Python 3.10 or higher https://www.python.org/downloads/

## Data Source

Individual contribution data can be downloaded from the [FEC.gov Bulk Data Download page](https://www.fec.gov/data/browse-data/?tab=bulk-data) under "Contributions by individuals". 

### Downloading and Preparing the Data

1. Choose the desired year range (e.g., "2023 - 2024").
2. Download the zip file and extract its contents.
3. Locate the `itcont.txt` file, which contains all records for the selected date range.
4. Rename `itcont.txt` to reflect the year range (e.g., `contributions_2023_2024.txt`).

The file structure is documented in the [FEC's Contributions by Individuals File Description](https://www.fec.gov/campaign-finance-data/contributions-individuals-file-description/).

## Tools

### 1. filter.py

Filters the downloaded data by Committee ID.

Usage:
python filter.py [-h] target_cmte_id input_file output_file

### 2. run_days.py 

Usage python run_days.py [-h] [--state STATE] [--start-date START_DATE] [--end-date END_DATE] [--csv CSV] file_path min_days max_days

Arguments:
- `file_path`: Path to the input file
- `min_days`: Minimum number of unique days to include
- `max_days`: Maximum number of unique days to include
- `--state STATE`: (Optional) Filter by two-letter state code (e.g., VA for Virginia, CA for California)
- `--start-date START_DATE`: (Optional) Start date for filtering
- `--end-date END_DATE`: (Optional) End date for filtering
- `--csv CSV`: (Optional) Flag to export results as CSV


### 3. run_count.py

Analyzes the data by total count of contributions.

Usage:
python run_count.py [-h] [--state STATE] [--start-date START_DATE] [--end-date END_DATE] [--csv CSV] file_path min_donations max_donations

Arguments:
- `file_path`: Path to the input file
- `min_donations`: Minimum number of donations to include
- `max_donations`: Maximum number of donations to include
- `--state STATE`: (Optional) Filter by two-letter state code (e.g., VA for Virginia)
- `--start-date START_DATE`: (Optional) Start date for filtering
- `--end-date END_DATE`: (Optional) End date for filtering
- `--csv CSV`: (Optional) Flag to export results as CSV
- 
## Example Workflow

1. Download data from FEC.gov for the desired year range.
2. Use `filter.py` to filter the data by a specific Committee ID.
3. Analyze the filtered data using either `run_count.py` or `run_days.py`.


## Disclaimer

This project is not affiliated with or endorsed by the Federal Election Commission.
