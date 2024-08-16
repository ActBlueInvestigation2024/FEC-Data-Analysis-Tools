import os

def merge_text_files(input_folder, output_file):
    try:
        file_list = [f for f in os.listdir(input_folder) if f.endswith('.txt')]
        # sort files 
        file_list.sort()

        # open the output file in append mode
        with open(output_file, 'a') as outfile:
            for file_name in file_list:
                file_path = os.path.join(input_folder, file_name)
                # read each file and append its content to the output file
                with open(file_path, 'r') as infile:
                    outfile.write(infile.read() + '\n')  

        print(f"All files from '{input_folder}' have been merged into '{output_file}'")

    except Exception as e:
        print(f"An error occurred: {e}")



