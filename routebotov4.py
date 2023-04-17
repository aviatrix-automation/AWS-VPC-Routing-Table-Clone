import argparse
import boto3
import csv

# Define the command line arguments
parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--csv', help='The path to the CSV file containing VPC IDs')
group.add_argument('--vpc-ids', nargs='+', help='The IDs of the VPCs (space separated)')

parser.add_argument('--region', help='The region name', required=True)
args = parser.parse_args()

# Initialize the AWS EC2 client
ec2 = boto3.client('ec2', region_name=args.region)

# Read the VPC IDs from the CSV file
if args.csv:
    vpc_ids = []
    with open(args.csv, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            vpc_ids.append(row[0])
else:
    vpc_ids = args.vpc_ids
    
for vpc_id in vpc_ids:
    # Retrieve the route tables for the current VPC
    route_tables = ec2.describe_route_tables(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])['RouteTables']
    
    # Create a new route table
    new_route_table = ec2.create_route_table(VpcId=vpc_id)
    new_route_table_id = new_route_table['RouteTable']['RouteTableId']

    main_route_table_id = ''
    for route_table in route_tables:
        for association in route_table['Associations']:
            if association['Main']:
                main_route_table_id = route_table['RouteTableId']
                break
        if main_route_table_id:
            break

    print(f"Main Route table is {main_route_table_id} in VPC: {vpc_id}")
    # Iterate over the list of route tables and duplicate them
    for route_table in route_tables:
        # Check if the route table is the main route table of the VPC
        if route_table['Associations'] and 'Main' in route_table['Associations'][0]:
            continue  # Skip the main route table

        # Duplicate the routes from the existing route table to the new route table
        for route in route_table['Routes']:
            if 'GatewayId' in route and not route['GatewayId'].startswith('local'):
                ec2.create_route(
                    DestinationCidrBlock=route['DestinationCidrBlock'],
                    GatewayId=route['GatewayId'],
                    RouteTableId=new_route_table_id
                )
            elif 'TransitGatewayId' in route:
                ec2.create_route(
                    DestinationCidrBlock=route['DestinationCidrBlock'],
                    TransitGatewayId='tgw-08bd8dcab1f3487eb',
                    RouteTableId=new_route_table_id
                )
            elif 'NatGatewayId' in route:
                ec2.create_route(
                    DestinationCidrBlock=route['DestinationCidrBlock'],
                    NatGatewayId=route['NatGatewayId'],
                    RouteTableId=new_route_table_id
                )
            elif 'VpcPeeringConnectionId' in route:
                ec2.create_route(
                    DestinationCidrBlock=route['DestinationCidrBlock'],
                    VpcPeeringConnectionId=route['VpcPeeringConnectionId'],
                    RouteTableId=new_route_table_id
                )
            elif 'InstanceId' in route:
                ec2.create_route(
                    DestinationCidrBlock=route['DestinationCidrBlock'],
                    VpcPeeringConnectionId=route['InstanceId'],
                    RouteTableId=new_route_table_id
                )
            elif 'NetworkInterfaceId' in route:
                ec2.create_route(
                    DestinationCidrBlock=route['DestinationCidrBlock'],
                    VpcPeeringConnectionId=route['NetworkInterfaceId'],
                    RouteTableId=new_route_table_id
                )
    print(f"New route table created with ID: {new_route_table_id} in VPC: {vpc_id}")
