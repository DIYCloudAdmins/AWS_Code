import boto3
import pandas as pd

ec2 = boto3.client('ec2')
response = ec2.describe_security_groups()

securityGroups = []

for securityGroup in response['SecurityGroups']:
    sg = {}
    sg['name'] = securityGroup['GroupName']
    sg['vpcId'] = securityGroup.get('vpc_id', None)
    sg['groupId'] = securityGroup['GroupId']
    sg['accountId'] = securityGroup['OwnerId']
    #outbound rules
    egressRules = []
    if len(securityGroup['IpPermissionsEgress']) != 0:
        for egressRule in securityGroup['IpPermissionsEgress']:
            ipRule = {}
            ipRule['egressIpProtocol'] = egressRule['IpProtocol']
            ipranges = []
            for ipRange in egressRule['IpRanges']:
                ipranges.append(ipRange['CidrIp'])
            ipRule['egressIpRange'] = ipRange
            ipRule['egressDescription'] = egressRule.get('Description', '')
            egressRules.append(ipRule)
    sg['egressRules'] = egressRules
    #inbound rules
    ingressRules = []
    if len(securityGroup['IpPermissions']) != 0:
        for Permission in securityGroup['IpPermissions']:
            ingressRule = {}
            
            ingressRule['inboundProtocol'] = Permission['IpProtocol']

            if 'FromPort' in Permission:
                ingressRule['fromPort'] = Permission['FromPort']
                ingressRule['toPort'] = Permission['ToPort']
            else:
                ingressRule['fromPort'] = ''
                ingressRule['toPort'] =''               
    
            ingressRule['ipProtocol'] = Permission['IpProtocol']
            ingressRule['IpRanges'] = Permission['IpRanges']
            ingressRule['userIdGroupPairs'] = Permission['UserIdGroupPairs']
            ingressRules.append(ingressRule)
    sg['ingressRules'] = ingressRules

    securityGroups.append(sg)

securityGroupDF = pd.DataFrame(securityGroups)
print(securityGroupDF.head())