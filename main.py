import csv

# Define a function to parse the text data
def parse_text_file(file_path):
    with open(file_path, 'r') as file:
        data = file.read().split('\n\n')  # Split records by double newlines

    parsed_data = []
    for record in data:
        lines = record.strip().split('\n')
        pmid = lines[0].split('- ')[1].strip()
        authors = []
        for line in lines:
            if line.startswith('FAU - '):
                author = line.split(' - ')[1].strip()
                authors.append(author)
            if line.startswith('AD  - '):
                address = line.split(' - ')[1].strip()
                if authors:
                    parsed_data.append([pmid, authors[-1], address])
    return parsed_data

# Save parsed data to a CSV file
def save_to_csv(parsed_data, output_file):
    with open(output_file, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['PMID', 'Author', 'Affiliation'])
        csvwriter.writerows(parsed_data)

# File paths
input_file = 'data.txt'  # Replace with your text file path
output_file = 'output.csv'  # Output CSV file

# Parse the text file and save it to CSV
parsed_data = parse_text_file(input_file)
save_to_csv(parsed_data, output_file)

print("fin")