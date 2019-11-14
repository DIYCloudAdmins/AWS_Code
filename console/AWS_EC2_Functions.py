import AWS_Helper_Functions as hf 


def getInstanceInfo(session: object, accountDict: dict, runningStates: list= ['running','stopped','stopping'])->dict:
    '''returns a list of dictionaries, one for each instance in an account
        session :valid session to an account
        accountDict: dictionary object with information about account being inspected
        runningStates = only instances whose running states are included in list will be returned'''

    session = session
    account = accountDict
    instanceList = []
    runningStates = runningStates

    ec2 = session.client('ec2')
    response = ec2.describe_instances(Filters=[{'Name':'instance-state-name','Values':runningStates}])

    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            instanceDict = {}
                        
            instanceDict['accountId'] = account['accountId']
            instanceDict['accountName'] = account['accountName']
            instanceDict['instanceId'] = instance['InstanceId']
            instanceDict['vpcId'] = instance.get('VpcId', None)

            if 'Tags' in instance.keys():
                instanceDict['project'] = hf.getTagValue(instance['Tags'],'Project')
                instanceDict['component'] = hf.getTagValue(instance['Tags'], 'Component')
                instanceDict['owner'] = hf.getTagValue(instance['Tags'], 'Owner')
                if hf.getTagValue(instance['Tags'], 'autoSchedule') != None:
                    instanceDict['autoSchedule'] = True
                else:
                    instanceDict['autoSchedule'] = False
            else:
                instanceDict['project'] = None
                instanceDict['component'] = None
                instanceDict['owner'] = None
                instanceDict['autoSchedule'] = False

            # assumes that the first network interface was created when the server was created
            try:
                instanceDict['creationTime'] = (instance['NetworkInterfaces'][0]['Attachment']['AttachTime'])
            except:
                instanceDict['creationTime'] = None
            instanceDict['subnetId'] = instance.get('SubnetId', None)
            instanceDict['instanceState'] = instance['State']['Name']
            instanceDict['hypervisor'] = instance['Hypervisor']
            instanceDict['launchTime'] = instance['LaunchTime']
            try:
                instanceDict['availibilityZone'] = instance['Placement']['AvailabilityZone']
            except:
                instanceDict['availibilityZone'] = None
            instanceDict['securityGroups'] = instance['SecurityGroups']
            instanceDict['publicIp'] = instance.get('PublicIpAddress', None)

            instanceList.append(instanceDict)

    return instanceList



def lookup_by_id(sgid):
    sg = ec2.get_all_security_groups(group_ids=sgid)
    return sg[0].name


def getUnusedSecurityGroups(session: object, accountDict: dict)->list:
    '''given a session object returns a list of unused
    security groups.  Looks at Instances, Classic ELB, 
    RDS, and VPCs'''


    session = session
    account = accountDict

    client = session.client('ec2')
    ec2 = session.resource('ec2')
    all_groups = []
    security_groups_in_use = []
    # Get ALL security groups names
    security_groups_dict = client.describe_security_groups()
    security_groups = security_groups_dict['SecurityGroups']
    for groupobj in security_groups:
        if groupobj['GroupName'] == 'default':
            security_groups_in_use.append(groupobj['GroupId'])
        all_groups.append(groupobj['GroupId'])

    # Get all security groups used by instances
    instances_dict = client.describe_instances()
    reservations = instances_dict['Reservations']
    network_interface_count = 0

    for i in reservations:
        for j in i['Instances']:
            for k in j['SecurityGroups']:
                if k['GroupId'] not in security_groups_in_use:
                    security_groups_in_use.append(k['GroupId'])
            # Security groups used by network interfaces
            for m in j['NetworkInterfaces']:
                network_interface_count += 1
                for n in m['Groups']:
                    if n['GroupId'] not in security_groups_in_use:
                        security_groups_in_use.append(n['GroupId'])

    # Security groups used by classic ELBs
    elb_client = session.client('elb')
    elb_dict = elb_client.describe_load_balancers()
    for i in elb_dict['LoadBalancerDescriptions']:
        for j in i['SecurityGroups']:
            if j not in security_groups_in_use:
                security_groups_in_use.append(j)

    # # Security groups used by ALBs
    # elb2_client = boto3.client('elbv2')
    # elb2_dict = elb2_client.describe_load_balancers()
    # for i in elb2_dict['LoadBalancers']:
    #     for j in i['SecurityGroups']:
    #         if j not in security_groups_in_use:
    #             security_groups_in_use.append(j)

    # Security groups used by RDS
    rds_client = session.client('rds')
    rds_dict = rds_client.describe_db_security_groups()

    for i in rds_dict['DBSecurityGroups']:
        for j in i['EC2SecurityGroups']:
            if j not in security_groups_in_use:
                security_groups_in_use.append(j)

    # Security groups used by VPCs
    vpc_dict = client.describe_vpcs()
    for i in vpc_dict['Vpcs']:
        vpc_id = i['VpcId']
        vpc = ec2.Vpc(vpc_id)
        for s in vpc.security_groups.all():
            if s.group_id not in security_groups_in_use:
                security_groups_in_use.append(s.group_id)

    delete_candidates = []
    for group in all_groups:
        if group not in security_groups_in_use:
            delete_candidates.append({'Account': account['accountName'], 'Group': group})

    return delete_candidates