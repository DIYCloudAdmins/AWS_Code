import boto3

def getSession(accountId:str, Role:str)->object:
    role = Role
    arn = 'arn:aws:iam::%s:role/%s' % (accountId, role)

    # if useEC2IAMRole:
    # boto3 STS code for instance IAM role
    sessionName = '%s-%s' % ("TagFlowDown", role)
    stsClient = boto3.client("sts")
    assumedRoleObject = stsClient.assume_role(
        RoleArn=arn,
        RoleSessionName=sessionName
    )
    credentials = assumedRoleObject['Credentials']
    accessKey = credentials['AccessKeyId']
    secretKey = credentials['SecretAccessKey']
    sessionToken = credentials['SessionToken']
    newSession = boto3.session.Session(aws_access_key_id=accessKey,
                                           aws_secret_access_key=secretKey,
                                           aws_session_token=sessionToken)
    return newSession


def getAccounts(ignoreNamedAccounts:list = [])->list:
    '''Returns a list of dictionaries with information regarding all
       accounts in the organization.  Accounts that should not be inlcuded
       can be passes as a list [account1, account2, account3]'''

    client = boto3.client('organizations')
    response = client.list_accounts()

    accountList = []

    while True:
        for i in response['Accounts']:
            if i['Name'] not in ignoreNamedAccounts:
                accountList.append(
                    {'accountArn': i['Arn'],
                    'accountId': i['Id'],
                    'accountName': i['Name'],
                    'accountEmail': i['Email'],
                    'accountStatus': i['Status']})

        nextToken = response.get('NextToken', None)

        if nextToken != None:
            response = client.list_accounts(NextToken=response['NextToken'])
        else:
            break

    return accountList

def getAccount(accountId: str)->dict:
    '''Returns a dictionary with information regarding a single
       account in the organization.'''

    client = boto3.client('organizations')
    response = client.describe_account(AccountId=accountId)

    accountDetails = {'accountArn': response['Account']['Arn'],
        'accountId': response['Account']['Id'],
        'accountName': response['Account']['Name'],
        'accountEmail': response['Account']['Email'],
        'accountStatus': response['Account']['Status']}

    return accountDetails


x = getAccount('511296683960')
print(x)