import boto3


def get_all__ec2_tags(instance_id :str, tags :list = [], missing_tag_value :str = '') ->list:
    """When given an instance ID as str e.g. 'i-1234567', and a list of tags as list e.g. ['Name', 'Environment' \
    return the tag values in a list (same order given). Change the value for missing tags by passing 'missing_tag_value'"""
        
    inst_id = instance_id
    tag_list = tags
    default_tag_value = missing_tag_value
    inst_tags = {}
    return_list = []

    ec2 = boto3.resource('ec2')
    ec2instance = ec2.Instance(inst_id)

    for tags in ec2instance.tags:
        inst_tags[tags['Key']] = tags['Value']

    for tag_name in tag_list:
        if tag_name in inst_tags:
            return_list.append(inst_tags[tag_name])
        else:
            return_list.append(default_tag_value)


    return return_list


def get_all_ec2_details(detail_type: str = 'id_only', header_row: str='yes') ->list:
    """returns a list of all ec2 instance \
       detail_type 'id_only' = returns a list of instance ids \
       'full_list' returns full list of instance information (check header \
       for full list of information) header_row 'no' = no header row included, \
       'yes' = first row will be header information, 'only' = Only return header row. 
       """
    list_detail = detail_type
    header_type = header_row
    instance_id_list = []
    ec2client = boto3.client('ec2')
    response = ec2client.describe_instances()

    instance_id_header_list =["InstanceId", 'InstanceType', 'State', 'VpcId', \
    'SubnetId', 'PrivateIpAddress', 'PrivateDnsName', 'AvailabilityZone', \
    'PublicDnsName', 'Architecture', 'Hypervisor', 'VirtualizationType', \
    'CoreCount', 'ThreadsPerCore']

    if header_type == 'yes':
        if list_detail == 'id_only':
            instance_id_list.append(['InstanceId'])
        instance_id_list.append(instance_id_header_list)
    elif header_type == 'only':
        if list_detail == 'id_only':
            return ['InstanceId']
        return instance_id_header_list


    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            if list_detail == 'full_list':
                instance_id_list.append([instance["InstanceId"] if "InstanceId" in instance else '' , instance['InstanceType'] if 'InstanceType' in instance else '', \
                instance['State']['Name'] if instance['State']['Name'] else '', instance['VpcId'] if 'VpcId' in instance else ''  , \
                instance['SubnetId'] if 'SubnetId' in instance else '', instance['PrivateIpAddress'] if 'PrivateIpAddress' in instance else '', \
                instance['PrivateDnsName'] if 'PrivateDnsName' in instance else '', instance['Placement']['AvailabilityZone'] if instance['Placement']['AvailabilityZone'] else '', \
                instance['PublicDnsName'] if 'PublicDnsName' in instance else '', instance['Architecture'] if 'Architecture' in instance else '', \
                instance['Hypervisor'] if 'Hypervisor' in instance else '', instance['VirtualizationType'] if 'VirtualizationType' in instance else '', \
                instance['CpuOptions']['CoreCount'] if instance['CpuOptions']['CoreCount'] else '', instance['CpuOptions']['ThreadsPerCore'] if instance['CpuOptions']['ThreadsPerCore'] else ''])
            elif list_detail == 'id_only':
                instance_id_list.append(instance['InstanceID']) 
            # This will print will output the value of the Dictionary key 'InstanceId'
    
    return instance_id_list


for item in get_all_ec2_details('full_list', 'yes'):
    print(item)

for item in get_all__ec2_tags('i-0df9e3147483fa4a1', ['Name', 'Address'], 'empty'):
    print(item)