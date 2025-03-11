import os
import sys
import csv

# python3 mergeCSVs.py ../../results/jsminer-out/ > collections-failed.txt

cwd = sys.argv[1]

output_file = 'results.csv'

delimiter = ','

csv_files = [f for f in os.listdir(cwd) if f.endswith('.csv')]

lost_lines = []
writed_lines = []

with open(output_file, 'w', newline='') as outfile:
    writer = None
    num_columns = None  # Variable to store the number of columns in the header

    for csv_file in csv_files:
        with open(os.path.join(cwd, csv_file), 'r') as infile:
            reader = csv.reader(infile, delimiter=delimiter)

            has_header = csv.Sniffer().sniff(infile.readline())
            infile.seek(0)

            if writer is None:
                writer = csv.writer(outfile, delimiter=delimiter)

                if has_header:
                    header = next(reader)
                    header = [col.replace('-', '_') for col in header]
                    writer.writerow(header)
                    num_columns = len(header)  # Get the number of columns from the header
                    # print(f"colunas: {num_columns}")
                    

            if has_header:
                next(reader)

            previous_row = None  # To store the previous row

            for row in reader:
                # print(f"linhas: {len(row)}")
                # sys.exit()
                if len(row) == num_columns:
                    # last_element = row[-1]
                    # if last_element == '':
                    #     row = list(filter(lambda x: x != '', row))
                    # # Check if files reduced by more than 50% compared to the previous row
                    # if previous_row is not None and int(row[3]) < 0.5 * int(previous_row[3]):
                    #     lost_lines.append(row)
                    # else:
                    writer.writerow(row)
                    writed_lines.append(row)
                    # Update the previous row for the next iteration
                    previous_row = row
                else:
                    lost_lines.append(row)

print('Merge finished:', output_file)
print('Writed lines:', len(writed_lines))
print('Lost lines:', len(lost_lines))

for line in lost_lines:
    print(line)