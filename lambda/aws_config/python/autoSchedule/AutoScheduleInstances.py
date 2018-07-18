import AS_Helper
import boto3
import json

def evaluateTag(tagValue):
    
    configlist = tagValue.split(";")

    returnMessage = "noAction"
    
    schedule = AS_Helper.evaluateSchedule(configlist)
    if ( 
        schedule.shutdown == True and schedule.shutdownHourMatch == True and schedule.shutdownToday == True
        ):
            returnMessage = "shutDown"
    if (
        schedule.startup == True and schedule.startupHourMatch == True and schedule.startupToday == True
        ):
            returnMessage = "startUp"
    return returnMessage

def identifyInstances():

    outMsg=[] 
    print("starting EC2 AutoScheduler")
    tagkey="autoSchedule"
    client=boto3.client('ec2')
    ec2inst=boto3.resource('ec2')
    response=client.describe_instances(
        Filters = [{'Name': 'tag:autoSchedule', 'Values': ['*']},{'Name': 'instance-state-name','Values': ['running']}]
    )
      
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            instanceID = instance["InstanceId"]
            EC2instance = ec2inst.Instance(instanceID)
            for tags in EC2instance.tags:
                if tags["Key"] == 'Name':
                    instanceName = (tags["Value"])
                if tags["Key"] == "autoSchedule":
                    tagSchedule = (tags["Value"])
                    tagAction = evaluateTag(tagSchedule)
            if tagAction == "shutDown":
                print(instanceID  + " - " + instanceName + " - stoping")
            if tagAction == "startUp":
                print(instanceID  + " - " + instanceName + " - starting")


    return "completed autoSchedule Sequence"

def lambda_handler(event, context):
    x = identifyInstances()
    print(x)
