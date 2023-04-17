This script allows you to duplicate the main route table of one or more Amazon Web Services (AWS) Virtual Private Clouds (VPCs). The duplicated route table can be used to make changes to the routing configuration without affecting the existing main route table.

# Prerequisites

Python 3.x

Boto3 Python library

AWS credentials configured on your system

# Installation

Install Python 3.x from the official website.

Install Boto3 Python library by running pip install boto3 on your command line.

# Usage

To run the script, execute the following command:

    python routebotov4.py --csv path/to/csv/file --region aws_region_name

OR

    python routebotov4.py --vpc-ids vpc_id_1 vpc_id_2 ... --region aws_region_name

Replace path/to/csv/file with the path to the CSV file containing the VPC IDs (one per line).

Replace aws_region_name with the name of the AWS region where your VPCs are located.

Use either the --csv or --vpc-ids argument, but not both.

# Output

The script creates a new route table for each VPC specified and duplicates the routes from the main route table to the new route table. The output includes the ID of the main route table, the ID of the new route table, and the VPC ID. If no main route table is found for a given VPC, a message is printed indicating that no main route table was found.
