import boto3
import json
 
def lambda_handler(event, context):
    outMsg=[]  
    outMsg.append("starting nightly stop of EC2 instances who are tagged OvernightTerm=Yes")
    print("starting nightly stop of EC2 instances who are tagged OvernightTerm=Yes")
    tagkey="OvernightTerm"
    client=boto3.client('ec2')
    ec2inst=boto3.resource('ec2')
    response=client.describe_instances(
        Filters = [{'Name': 'tag:OvernightTerm', 'Values': ['Yes']},{'Name': 'instance-state-name','Values': ['running']}]
    )
      
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            instanceID = instance["InstanceId"]
            EC2instance = ec2inst.Instance(instanceID)
            for tags in EC2instance.tags:
                if tags["Key"] == 'Name':
                    instanceName = (tags["Value"])
            print(instanceID  + " - " + instanceName + ": stopping")
            msg = instanceID
            outMsg.append(msg)        
            id=[instanceID]

# client.stop_instances(InstanceIds=id)
    snsclient = boto3.client('sns')
    response = snsclient.publish(
        TargetArn="arn:aws:sns:us-east-1:511296683960:EC2_AutoStop",
        Message=json.dumps(outMsg, sort_keys=True, indent=4, separators=(',', ': '))
    )
        
    return "completed stopping instances"
