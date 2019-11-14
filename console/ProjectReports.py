import boto3
import pandas as pd 
import matplotlib as mp 
import csv
import AWS_SessionManager as sm 
import AWS_EC2_Functions as ecf 
import AWS_Helper_Functions as hf 
import AWS_MessageWriter as mw


if __name__ == '__main__':
    accounts =  sm.getAccounts()

    unaccessableAccounts = []
    role = 'Virtualization_Admins'

    messages = []

    
    i=1
    unUsedSecurityGroups = []

    #Build Master DataFrames and Lists
    for account in accounts:
        session = sm.getSession(account['accountId'], role)
        if session !=None:  
            accountInstances = ecf.getInstanceInfo(session, account)
            unusedSGroups =  ecf.getUnusedSecurityGroups(session, account)
            
            if len(accountInstances) > 0:
                if i == 1:
                    EC2DataFrame = pd.DataFrame(accountInstances, columns=accountInstances[0].keys())
                    i+=1
                else:
                    EC2DataFrame = EC2DataFrame.append(accountInstances, ignore_index=True, sort=True)
            
            if len(unusedSGroups) > 0:
                unUsedSecurityGroups.append(unusedSGroups)

        else:
            unaccessableAccounts.append({'accountName': account['accountName'], 'AccountID': account['accountId'], 'role': role})

        

    # build unaccessable account message:
    if len(unaccessableAccounts) != 0:
        aAccounts = pd.DataFrame(unaccessableAccounts)
        message = mw.messageSection('Critical: The Following Accounts Are inaccessable')
        message.description = f'Listed accounts were not accessable with the role: {role}'
        message.message = aAccounts.to_html(index=False)
        messages.append(message)

    
    # build unused security group message:
    if len(unUsedSecurityGroups) !=0:
        uGroups = pd.DataFrame(unUsedSecurityGroups)
        message = mw.messageSection('Critical: Disconnected Security Groups')
        message.description = f'The following Security groups do not appear to be associated with a resource'
        message.message = uGroups.to_html(index=False)
        messages.append(message)


    # build missing Project Tag message:
    noProjectDataFrame = EC2DataFrame[EC2DataFrame.project.isnull()][['vpcId','accountName', 'instanceId', 'instanceState']]
    if len(noProjectDataFrame.columns) !=0:
        message = mw.messageSection('Critical: Instances without Project Tag')
        message.description = f'The following instances are missing the Project Tag'
        message.message = noProjectDataFrame.to_html(index=False)
        messages.append(message)
    

with open('output.html', 'w') as out_file:
    for m in messages:
        out_file.write(str(m))
