# DMARC XML Parsing and Analysis Script

This script parses DMARC XML files, extracts relevant information, and performs reverse DNS lookups on source IP addresses. The parsed data is then saved to a CSV file.

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Notes](#notes)

## Requirements

- Python 3.x
- The following Python packages:
  - `os`
  - `xml.etree.ElementTree`
  - `pandas`
  - `socket`
  - `tqdm`
  - `dmarc`

## Installation

1. Clone this repository or download the script.

2. Install the required Python packages using pip:
    ```bash
    pip install pandas tqdm dmarc
    ```

## Usage

1. Modify the script to specify the correct paths for the source and destination directories:
    ```python
    source_directory = r'C:\Users\test\path\source'
    destination_directory = r'C:\Users\test\path\dest'
    ```

2. Run the script:
    ```bash
    python script.py
    ```

3. The parsed data will be saved to `path.csv` in the specified destination directory.

## How It Works

1. **Reverse DNS Lookup**:
    - The `reverse_dns_lookup` function takes an IP address and checks if it has already been resolved. If not, it performs a reverse DNS lookup to find the associated host name.

2. **DMARC XML Parsing**:
    - The `parse_dmarc_xml` function parses DMARC XML files, extracts information about emails that did not pass DMARC checks, and appends this data to a list.

3. **Main Execution Flow**:
    - The `main` function handles the overall flow:
        - Checks if the source and destination directories exist.
        - Iterates through each XML file in the destination directory, parsing them and collecting records.
        - Performs reverse DNS lookups on the collected records.
        - Converts the records to a pandas DataFrame and saves it to a CSV file.

## Notes

- Ensure that the source and destination directories contain the appropriate XML files for parsing.
- The script includes a progress bar for both XML parsing and reverse DNS lookups for better user experience.
- Duplicate records are handled by summing the email counts of the duplicates.

## Example

Here is an example of the output after running the script:

```
   source_ip_address policy_disposition dkim_alignment spf_alignment    from_domain      dkim_domain dkim_result       spf_domain spf_result      source_domain_name  mail_count
0    192.0.2.1         reject              fail              pass              example.com    example.org         fail               example.net       pass                  mail.example.com          10
1    198.51.100.2      quarantine          pass              fail              another.com    another.org         pass               another.net       fail                  mail.another.com        5
```

This output will be saved to a CSV file specified in the script.
