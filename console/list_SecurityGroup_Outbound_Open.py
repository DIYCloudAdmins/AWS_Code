import boto3
ec2 = boto3.client('ec2')
response = ec2.describe_security_groups()

for securityGroups in response['SecurityGroups']:
    for ipEgress in securityGroups['IpPermissionsEgress']:
        for ipRange in ipEgress['IpRanges']:
            if ipRange ['CidrIp'] == "0.0.0.0/0":
                print("Name: " + securityGroups['GroupName'] + ",  ID:" + securityGroups['GroupId'])

 
#  to add a filter to run against a single vpc add filter to describe_security_groups.
#     Filters=[
#         {
#             "Name":"vpc-id", "Values":["vpcID"]
#         }
#     ]
