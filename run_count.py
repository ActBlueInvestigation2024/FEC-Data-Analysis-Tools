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

def count_individual_contributors(file_path, min_donations, max_donations, start_date=None, end_date=None, state_code=None):
    # File description: https://www.fec.gov/campaign-finance-data/contributions-individuals-file-description/
    contributor_counts = defaultdict(int)
    contributor_amounts = defaultdict(float)
    contributor_employments = defaultdict(set)
    
    if start_date:
        start_date = parse_date(start_date, '%m%d%Y')
    if end_date:
        end_date = parse_date(end_date, '%m%d%Y')
    
    with open(file_path, 'r') as file:
        for line in file:
            fields = line.strip().split('|')
            
            if len(fields) < 15:
                continue

            try:
                entity_type = fields[6].strip()
                name = fields[7].strip()
                zip_code = fields[10].strip()
                state = fields[9].strip()
                
                transaction_amt_str = fields[14].strip()
                if transaction_amt_str:
                    try:
                        transaction_amt = float(transaction_amt_str)
                    except ValueError:
                        continue
                else:
                    continue
                
                transaction_date = parse_date(fields[13].strip(), '%m%d%Y')
                if transaction_date is None:
                    continue
                
                if (start_date and transaction_date < start_date) or (end_date and transaction_date > end_date):
                    continue
                
                employment_status = fields[11].strip()
                
                if entity_type == 'IND' and (state_code is None or state == state_code):
                    key = (name, zip_code)
                    contributor_counts[key] += 1
                    contributor_amounts[key] += transaction_amt
                    contributor_employments[key].add(employment_status)
            
            except IndexError:
                continue
    
    filtered_contributors = {
        key: (
            contributor_counts[key],
            contributor_amounts[key],
            contributor_employments[key]
        )
        for key in contributor_counts
        if min_donations <= contributor_counts[key] <= max_donations
    }
    
    sorted_contributors = sorted(
        filtered_contributors.items(),
        key=lambda item: item[1][0],  # sort by number of donations
        reverse=True
    )
    
    total_amount = sum(amount for _, amount, _ in filtered_contributors.values())
    total_contributors = len(filtered_contributors)
    
    return sorted_contributors, total_amount, total_contributors

def export_to_csv(contributors, total_amount, total_contributors, output_file):
    # CSV export
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['Name', 'ZIP Code', 'Number of Donations', 'Total Amount', 'Employment Status']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for (name, zip_code), (count, amount, employments) in contributors:
            employment_list = ', '.join(employments) if employments else "Unknown"
            writer.writerow({
                'Name': name,
                'ZIP Code': zip_code,
                'Number of Donations': count,
                'Total Amount': f"${amount:.2f}",
                'Employment Status': employment_list
            })
        writer.writerow({})
        writer.writerow({
            'Name': 'Total',
            'ZIP Code': '',
            'Number of Donations': total_contributors,
            'Total Amount': f"${total_amount:.2f}",
            'Employment Status': ''
        })

def main():
    parser = argparse.ArgumentParser(description="Filter and analyze individual contributions.")
    parser.add_argument('file_path', type=str, help="Path to the input .txt file")
    parser.add_argument('min_donations', type=int, help="Minimum number of donations to filter by")
    parser.add_argument('max_donations', type=int, help="Maximum number of donations to filter by")
    parser.add_argument('--state', type=str, help="State code to filter by (two-letter code)")
    parser.add_argument('--start-date', type=str, help="Start date for the date range filter (MMDDYYYY)")
    parser.add_argument('--end-date', type=str, help="End date for the date range filter (MMDDYYYY)")
    parser.add_argument('--csv', type=str, help="Path to output CSV file (optional)")

    args = parser.parse_args()
    
    contributors, total_amount, total_contributors = count_individual_contributors(
        args.file_path, args.min_donations, args.max_donations, args.start_date, args.end_date, args.state
    )
    
    print(f"Number of individual contributors with between {args.min_donations} and {args.max_donations} donations: {total_contributors}")
    for (name, zip_code), (count, amount, employments) in contributors:
        employment_list = ', '.join(employments) if employments else "Unknown"
        print(f"Name: {name}, ZIP Code: {zip_code}, Number of Donations: {count}, Total Amount: ${amount:.2f}, Employment Status: {employment_list}")
    
    print(f"Total amount contributed by individuals with between {args.min_donations} and {args.max_donations} donations: ${total_amount:.2f}")
    print(f"Total number of such contributors: {total_contributors}")

    if args.csv:
        export_to_csv(contributors, total_amount, total_contributors, args.csv)
        print(f"Results have been exported to {args.csv}")

if __name__ == "__main__":
    main()
