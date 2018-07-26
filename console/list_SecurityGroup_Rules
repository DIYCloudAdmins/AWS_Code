import boto3
ec2 = boto3.client('ec2')
response = ec2.describe_security_groups()
for securityGroups in response['SecurityGroups']:
    print("Security Group Name: "+securityGroups['GroupName'])
    print("Egress Rules: ")
    for egressRules in securityGroups['IpPermissionsEgress']:
        print("IP Protocol: "+egressRules['IpProtocol'])
        for ipRange in egressRules['IpRanges']:
            print("IP Ranges: "+ipRange['CidrIp'])
    print("Ingress Rules: ")
    for Permissions in securityGroups['IpPermissions']:
        print("IP Protocol: "+Permissions['IpProtocol'])
        try:
            print("PORT: "+str(Permissions['FromPort']))
            for ipRange in Permissions['IpRanges']:
                print("IP Ranges: "+ipRange['CidrIp'])
        except Exception:
            print("No Port")
            continue
