import os
import xml.etree.ElementTree as ET
from dmarc import DMARC
import pandas as pd
import socket
from tqdm import tqdm

def reverse_dns_lookup(ip_address, seen_dns):
    if ip_address in seen_dns:
        return seen_dns[ip_address]
    else:
        try:
            # Use gethostbyaddr to obtain the host name associated with the IP address
            host_name, _, _ = socket.gethostbyaddr(ip_address)
            return host_name
        except socket.herror:
            # Handle errors if the IP address does not have an associated host name
            return None

# Function to parse a DMARC XML file with a progress bar
def parse_dmarc_xml(file_path, records_list, mail_counts):
    tree = ET.parse(file_path)
    root = tree.getroot()

    records = []
    record_elements = root.findall('.//record')
    
    for record in tqdm(record_elements, desc=f"Parsing {os.path.basename(file_path)}", leave=False):
        if (record.findtext('.//policy_evaluated/dkim') not in ["pass"] or record.findtext('.//auth_results/dkim/result') not in ["pass"]) and (record.findtext('.//policy_evaluated/spf') not in ["pass"] or record.findtext('.//auth_results/spf/result') not in ["pass"]):
            row = {}
            row['source_ip_address'] = record.findtext('.//source_ip')
            row['policy_disposition'] = record.findtext('.//policy_evaluated/disposition')
            row['dkim_alignment'] = record.findtext('.//policy_evaluated/dkim')
            row['spf_alignment'] = record.findtext('.//policy_evaluated/spf')
            row['from_domain'] = record.findtext('.//identifiers/header_from')
            row['dkim_domain'] = record.findtext('.//auth_results/dkim/domain')
            row['dkim_result'] = record.findtext('.//auth_results/dkim/result')
            row['spf_domain'] = record.findtext('.//auth_results/spf/domain')
            row['spf_result'] = record.findtext('.//auth_results/spf/result')
            
            if row in records_list:
                # Find the index of the duplicate in records_list
                # Add the number of emails to the existing record
                index = mail_counts.index(row) + 1
                mail_counts[index] += int(record.findtext('.//count'))
            else:
                mail_counts.append(row)
                mail_counts.append(int(record.findtext('.//count')))
                records.append(row)
    return records

def main():
    source_directory = r'C:\Users\test\path\source'
    destination_directory = r'C:\Users\test\path\dest'

    # Check if the destination directory exists, otherwise create it
    if not os.path.exists(destination_directory) and not os.path.exists(source_directory):
        print(f"Directory not found {destination_directory} or {source_directory}")
        exit(1)

    # List to store all records
    all_records = []
    seen_dns = {}
    mail_counts = []

    # Iterate over each XML file in the folder with a progress bar
    for filename in tqdm(os.listdir(destination_directory), desc="Parsing XML files"):
        if filename.endswith('.xml'):
            file_path = os.path.join(destination_directory, filename)
            records = parse_dmarc_xml(file_path, all_records, mail_counts)
            all_records.extend(records)

    for i in range(0, len(mail_counts), 2):
        mail_counts[i]["mail_count"] = mail_counts[i + 1]

    # Add a progress bar for reverse DNS lookup
    for record in tqdm(all_records, desc="Performing reverse DNS lookups"):
        resolved = reverse_dns_lookup(record["source_ip_address"], seen_dns)
        record["source_domain_name"] = resolved
        seen_dns[record["source_ip_address"]] = resolved

    # Convert the records to a pandas DataFrame
    df = pd.DataFrame(all_records)

    # Display the first few rows of the DataFrame
    print(df.head())

    # Save the DataFrame to a CSV file
    df.to_csv(r'C:\Users\test\path.csv', index=False)

if __name__ == "__main__":
    main()
