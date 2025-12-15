import csv

def parse_text_file(file_path):
    parsed_data = []
    current_pmid = None
    current_author_index = None
    collecting_affiliation = False

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            raw_line = line.rstrip('\n')

            # Empty line → stop collecting affiliation
            if not raw_line.strip():
                collecting_affiliation = False
                continue

            # PMID
            if raw_line.startswith('PMID-'):
                current_pmid = raw_line.split('-', 1)[1].strip()
                collecting_affiliation = False

            # FAU
            elif raw_line.startswith('FAU -') and current_pmid:
                author = raw_line.split('-', 1)[1].strip()
                parsed_data.append([current_pmid, author, "-"])
                current_author_index = len(parsed_data) - 1
                collecting_affiliation = False

            # Start of affiliation
            elif raw_line.startswith('AD  -') and current_author_index is not None:
                affiliation = raw_line.split('-', 1)[1].strip()
                parsed_data[current_author_index][2] = affiliation
                collecting_affiliation = True

            # Continuation of affiliation (indented line)
            elif collecting_affiliation and raw_line.startswith('      '):
                parsed_data[current_author_index][2] += " " + raw_line.strip()

            else:
                collecting_affiliation = False

    return parsed_data


def save_to_csv(parsed_data, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['PMID', 'Author', 'Affiliation'])
        writer.writerows(parsed_data)


# Files
input_file = 'pubmed-monoclonal-set.txt'
output_file = 'output.csv'

parsed_data = parse_text_file(input_file)
save_to_csv(parsed_data, output_file)

print("fin")
