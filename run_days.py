from datetime import datetime
import argparse
import csv
from collections import defaultdict

def parse_date(date_str, date_format='%m%d%Y'):
    if not date_str.strip():
        return None  
    try:
        return datetime.strptime(date_str, date_format)
    except ValueError:
        return None  

def count_individual_contributors(file_path, min_days, max_days, start_date=None, end_date=None, state_code=None):
    # File description: https://www.fec.gov/campaign-finance-data/contributions-individuals-file-description/
    # ----
    # python dictionary to keep track of counts, total amounts, and employment status
    contributor_counts = defaultdict(int)
    contributor_amounts = defaultdict(float)
    contributor_employments = defaultdict(set)
    contributor_dates = defaultdict(set)
    
    # convert the start_date and end_date to datetime objects for comparison
    if start_date:
        start_date = parse_date(start_date, '%m%d%Y')
    if end_date:
        end_date = parse_date(end_date, '%m%d%Y')
    
    with open(file_path, 'r') as file:
        for line in file:
            # split the line by the delimiter '|'
            fields = line.strip().split('|')
            
            # Skip lines that do not have the expected number of fields
            if len(fields) < 15:
                continue

            try:
                # extract entity_type, name, ZIP, and state fields
                entity_type = fields[6].strip()
                name = fields[7].strip()
                zip_code = fields[10].strip()
                state = fields[9].strip()
                
                # handle possible empty or invalid transaction amount
                transaction_amt_str = fields[14].strip()
                if transaction_amt_str:
                    try:
                        transaction_amt = float(transaction_amt_str)
                    except ValueError:
                        continue
                else:
                    continue
                
                # extract and parse the transaction date
                transaction_date = parse_date(fields[13].strip(), '%m%d%Y')
                if transaction_date is None:
                    # skip record if the date is invalid
                    continue
                
                # filter by date range
                if (start_date and transaction_date < start_date) or (end_date and transaction_date > end_date):
                    continue
                
                employment_status = fields[11].strip()  # Employer
                
                # Check if the entity type is 'IND' (Individual) and if it matches the state filter
                if entity_type == 'IND' and (state_code is None or state == state_code):
                    key = (name, zip_code)
                    contributor_counts[key] += 1
                    contributor_amounts[key] += transaction_amt
                    contributor_employments[key].add(employment_status)
                    contributor_dates[key].add(transaction_date.date())
            
            except IndexError:
                # skip lines where there is not enough fields to process
                continue
    
    # filter contributors with unique donation days within the specified range
    filtered_contributors = {
        key: (
            contributor_counts[key],
            contributor_amounts[key],
            contributor_employments[key],
            len(contributor_dates[key])  # Number of unique donation days
        )
        for key in contributor_counts
        if min_days <= len(contributor_dates[key]) <= max_days
    }
    
    # sort contributors by the number of unique donation days in descending order
    sorted_contributors = sorted(
        filtered_contributors.items(),
        key=lambda item: item[1][3],  # sort by unique days
        reverse=True
    )
    
    # calculate total amount and total number of contributors
    total_amount = sum(amount for _, amount, _, _ in filtered_contributors.values())
    total_contributors = len(filtered_contributors)
    
    return sorted_contributors, total_amount, total_contributors

def export_to_csv(contributors, total_amount, total_contributors, output_file):
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['Name', 'ZIP Code', 'Contributions', 'Total Amount', 'Employment Status', 'Unique Donation Days']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for (name, zip_code), (count, amount, employments, unique_days) in contributors:
            employment_list = ', '.join(employments) if employments else "Unknown"
            writer.writerow({
                'Name': name,
                'ZIP Code': zip_code,
                'Contributions': count,
                'Total Amount': f"${amount:.2f}",
                'Employment Status': employment_list,
                'Unique Donation Days': unique_days
            })
        # write the totals at the end
        writer.writerow({})
        writer.writerow({
            'Name': 'Total',
            'ZIP Code': '',
            'Contributions': total_contributors,
            'Total Amount': f"${total_amount:.2f}",
            'Employment Status': '',
            'Unique Donation Days': ''
        })

def main():
    # Command line arguments
    parser = argparse.ArgumentParser(description="Filter and analyze individual contributions.")
    parser.add_argument('file_path', type=str, help="Path to the input .txt file")
    parser.add_argument('min_days', type=int, help="Minimum number of unique donation days to filter by")
    parser.add_argument('max_days', type=int, help="Maximum number of unique donation days to filter by")
    parser.add_argument('--state', type=str, help="State code to filter by (two-letter code)")
    parser.add_argument('--start-date', type=str, help="Start date for the date range filter (MMDDYYYY)")
    parser.add_argument('--end-date', type=str, help="End date for the date range filter (MMDDYYYY)")
    parser.add_argument('--csv', type=str, help="Path to output CSV file (optional)")

    args = parser.parse_args()
    
    # process the file and get results
    contributors, total_amount, total_contributors = count_individual_contributors(
        args.file_path, args.min_days, args.max_days, args.start_date, args.end_date, args.state
    )
    

    print(f"Number of individual contributors with between {args.min_days} and {args.max_days} unique donation days: {total_contributors}")
    for (name, zip_code), (count, amount, employments, unique_days) in contributors:
        employment_list = ', '.join(employments) if employments else "Unknown"
        print(f"Name: {name}, ZIP Code: {zip_code}, Contributions: {count}, Total Amount: ${amount:.2f}, Employment Status: {employment_list}, Unique Donation Days: {unique_days}")
    
    print(f"Total amount contributed by individuals with between {args.min_days} and {args.max_days} unique donation days: ${total_amount:.2f}")
    print(f"Total number of such contributors: {total_contributors}")

    # Export to CSV if  option flag
    if args.csv:
        export_to_csv(contributors, total_amount, total_contributors, args.csv)
        print(f"Results have been exported to {args.csv}")

if __name__ == "__main__":
    main()
