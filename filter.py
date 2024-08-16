import argparse

def filter_committees(input_file_path, output_file_path, target_cmte_id):
    with open(input_file_path, 'r') as infile, open(output_file_path, 'w') as outfile:
        for line in infile:
            # split the line by the delimiter '|' (view data structure here: 
            fields = line.strip().split('|')
            
            # Get the commitee ID field
            cmte_id = fields[0]
            
            # check if the CMTE_ID matches the target committee ID
            if cmte_id == target_cmte_id:
                # write the line to the output file
                outfile.write(line)

def main():
    parser = argparse.ArgumentParser(description='Filter records by committee ID.')
    
    # command-line arguments
    parser.add_argument('target_cmte_id', type=str, help='Target committee ID to filter by.')
    parser.add_argument('input_file', type=str, help='The path to the input file.')
    parser.add_argument('output_file', type=str, help='The path to the output file.')
    
    args = parser.parse_args()
    
    # call the filter_committees function with the parsed arguments
    filter_committees(args.input_file, args.output_file, args.target_cmte_id)
    print(f"Filtered records have been written to {args.output_file}")

if __name__ == '__main__':
    main()

