'''Script to identify ec2 instances with no project tags.
          If instance is older than specified number of hours
          and if instance does not have a project tag
          lack of project tag will be reported.
          if instnces is older than second specified number of hours
          and if instance does not have a project tag it will reported and
          TERMINATED'''

import boto3
import json
from datetime import datetime, timezone


def ProjectTag(listOfTagDicts: list)->bool:
        tagList = listOfTagDicts

        for tags in tagList:
            if tags['Key'] == 'Project':
                return True
        
        return False


def notificationText(listToReport: list, listToTerminate, reportTime: int, terminateTime: int) ->str:
    retText = f"""<br> It is policy that new instances be tagged when created.  Instances not tagged within {terminateTime} hours
    will be terminated.  <b>All information associated with these instances will be lost </b> <br>"""
    
    if len(listToReport) > 0:
        retText = f'{retText}A scan of EC2 instances shows the following instances have been created for {reportTime} hours <br>'    
        for i in listToReport:
            retText = f'{retText}{i} <br>'
        
    if len(listToTerminate) > 0:
        retText = f"""{retText} <br> A scan of EC2 instances shows the following instance have been created for 
        more than {terminateTime} hours and will be <b>TERMINATED </b> <br>"""

        for i in listToTerminate:
            retText = f'{retText}{i} <br>'

    retText = f'{retText} <br><br> If you have questions of concerns please reach out to Paul Beauvais'

    return retText


def hoursSinceCreation(creationTime: datetime)->bool:
    '''Accepts a time stamp and returns number of hours passed'''

    timeDiff = datetime.now(timezone.utc) - creationTime
    hoursSinceCreation = (int(timeDiff.seconds)/60)/60
    
    return hoursSinceCreation

def sendSeS(emailText: str):

    sesClient = boto3.client('ses')

    emailSendAddresses = ['Paul.Beauvais@hibu.com']
    emailFromAddress = 'Paul.Beauvais@hibu.com'

    subject = 'Critical Warning - EC2 Instance Terminations'
    msgBody = emailText

    message = {'Subject': {'Data': subject}, 'Body': {'Html': {'Data': msgBody}}}

    response = sesClient.send_email(Source= emailFromAddress, Destination = {'ToAddresses': emailSendAddresses}, Message = message)




if __name__ == '__main__':

    # set to True if script should terminate instances without project tags
    # That have been active longer that the Terminate Time
    teminateActive = False

    reportTime = 2
    terminateTime = 6
    
    ec2client = boto3.client('ec2')
    response = ec2client.describe_instances(Filters=[{'Name':'instance-state-name','Values':['running','stopped','stopping']}])

    noTagList = []
    reportList = []
    terminateList = []

    
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:

            tempReportDict = {}
            tempTerminateDict = {}

            if 'Tags' in instance.keys():
                hasProjectTag = ProjectTag(instance["Tags"])
            else:
                hasProjectTag = False
            
            if hasProjectTag == False:
                #get first network interface for server, the attachement of the first interface
                #will generally give the uptime of the server
                creationInterval = hoursSinceCreation(instance['NetworkInterfaces'][0]['Attachment']['AttachTime'])

                if creationInterval >= reportTime and creationInterval < terminateTime:
                    tempReportDict['instanceId'] = instance['InstanceId']
                    tempReportDict['subnetId'] = instance['SubnetId'] if 'SubnetId' in instance else 'Not in Subnet'
                    tempReportDict['instanceState'] = instance['State']['Name']
                elif creationInterval >= terminateTime:
                    tempTerminateDict['instanceId'] = instance['InstanceId']
                    tempTerminateDict['subnetId'] = instance['SubnetId'] if 'SubnetId' in instance else 'Not in Subnet'
                    tempTerminateDict['instanceState'] = instance['State']['Name']

                if len(tempReportDict) > 0:
                    reportList.append(tempReportDict)
                
                if len(tempTerminateDict) > 0:
                    terminateList.append(tempTerminateDict)


    emailText = notificationText(reportList, terminateList, reportTime, terminateTime)

    print(emailText)
    sendSeS(emailText)
