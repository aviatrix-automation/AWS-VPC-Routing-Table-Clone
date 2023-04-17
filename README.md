# AWS-VPC-Routing-Table-Cloner
This repository contains code to duplicate VPC routing tables in a particular VPC.

In some instances its easier to duplicate a routing table and move the Main routing to a new one rather than deleting and creating a new one. This helps reduce the downtime required between delete and readding routes.

This code aims to automates the identification of the Main routing table in a VPC and duplicates it. You can modify the next-hops in the new routing table and then change to Main for a seamless migration.

# Usage 
Version 1.0:

    Identify the VPCs in which you want to duplicate the Main routing table.
    Create a CSV file with the list of VPC.
    Run the script as shown below:
    
    python3 routebotov4.py --region <AWS Region Name> --csv <CSV file name>
