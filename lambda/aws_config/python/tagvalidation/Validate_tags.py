#
# This file made available under CC0 1.0 Universal (https://creativecommons.org/publicdomain/zero/1.0/legalcode)
#
# Ensure that resources have required tags, and that tags have valid values.
#
# Trigger Type: Change Triggered
# Scope of Changes: EC2:Instance
# Accepted Parameters: requiredTagKey1, requiredTagValues1, requiredTagKey2, ...
# Example Values: 'CostCenter', 'R&D,Ops', 'Environment', 'Stage,Dev,Prod', ...
#                 An asterisk '*' as the value will just check that any value is set for that key

#Modified by Paul Beauvais - Source https://github.com/awslabs/aws-config-rules/blob/master/python/ec2_require_tags_with_valid_values.py



import boto3
import json
from datetime import datetime as dt, timedelta
from dateutil import relativedelta as rt


# Specify desired resource types to validate
APPLICABLE_RESOURCES = ["AWS::EC2::Instance"]


# Iterate through required tags ensureing each required tag is present, 
# and value is one of the given valid values
def find_violation(current_tags, required_tags):
    violation = ""
    for rtag,rvalues in required_tags.iteritems():
        tag_present = False
        for tag in current_tags:
            if tag['key'] == rtag:
                value_match = False
                tag_present = True
                rvaluesplit = rvalues.split(",")
                for rvalue in rvaluesplit:
                    if tag['value'] == rvalue:
                        value_match = True
                    if tag['value'] != "":
                        if rvalue == "*":
                            value_match = True
                if value_match == False:
                    violation = violation + "\n" + tag['value'] + " doesn't match any of " + required_tags[rtag] + "!"
        if not tag_present:
            violation = violation + "\n" + "Tag " + str(rtag) + " is not present."
    if violation == "":
        return None
    return  violation

def evaluate_compliance(configuration_item, rule_parameters):
    
    ec2 = boto3.resource('ec2')
    instance = ec2.Instance(configuration_item["resourceId"])
    
    if configuration_item["resourceType"] not in APPLICABLE_RESOURCES:
        return {
            "compliance_type": "NOT_APPLICABLE",
            "annotation": "The rule doesn't apply to resources of type " +
            configuration_item["resourceType"] + "."
        }

    if configuration_item["configurationItemStatus"] == "ResourceDeleted":
        return {
            "compliance_type": "NOT_APPLICABLE",
            "annotation": "The configurationItem was deleted and therefore cannot be validated."
        }
    #filter out legacy VPC
    if instance.vpc_id != "vpc-a859a8c6":
         return {
            "compliance_type": "NOT_APPLICABLE",
            "annotation": "This resource resides in the legacy VPC"
        }
    current_tags = configuration_item["configuration"].get("tags")
    
    violation = find_violation(current_tags, rule_parameters)        

    if violation:
        volumes = instance.volumes.all()
        for v in volumes:
            print(v.id)
            devices = [d['Device'] for d in v.attachments]
            for x in devices:
                violationExtention = "...disk = " + x + " ...... "
                volCreateTime = v.create_time.replace(tzinfo=None)
                relTime = rt.relativedelta(dt.now(), volCreateTime)
                reportList = []
                shutdownList = []
                terminateList = []
                sendReportMessage = False
                sendshutdownMessage = False
                sendTerminateMessage = False
                violationHours =  int(relTime.hours)
                violationDays = int(relTime.days)
                print(violationHours)
                print(violationDays)
                if (violationHours < 4 and violationDays == 0):
                    sendReportMessage = False
                    violationExtention = violationExtention + "instance " + configuration_item["resourceId"] + " is within expected time frame."
                    print(violationExtention)
                    break
                if ((violationHours >= 4 and violationHours < 10) and violationDays == 0):
                    sendReportMessage = True
                    reportList.append(configuration_item["resourceId"])
                    violationExtention = violationExtention + "instance " + configuration_item["resourceId"] + " will be shutdown soon!"
                    print(violationExtention)
                    break
                if ((violationHours >=10 and violationDays > 0) and violationDays < 5):
                    sendshutdownMessage = True
                    shutdownList.append(configuration_item["resourceId"])
                    violationExtention = violationExtention + "instance " + configuration_item["resourceId"] + " is being shutdown, and will be terminated soon!"
                    print(violationExtention)
                    print("shutdown")
                    break
                if (violationDays >= 5):
                    sendTerminateMessage = True
                    terminateList.append(configuration_item["resourceId"])
                    violationExtention = violationExtention + "instance " + configuration_item["resourceId"] + " is being terminated!  "
                    print (violationExtention)
                    break
        return {
            "compliance_type": "NON_COMPLIANT",
            "annotation": violation + "\r\n" + "....root disk created " + str(violationDays) + " days and " + str(violationHours) + " hours ago." + "\r\n" + violationExtention 
        }

    return {
        "compliance_type": "COMPLIANT",
        "annotation": "This resource is compliant with the rule."
    }

def lambda_handler(event, context):

    invoking_event = json.loads(event["invokingEvent"])
    configuration_item = invoking_event["configurationItem"]
    rule_parameters = json.loads(event["ruleParameters"])

    result_token = "No token found."
    if "resultToken" in event:
        result_token = event["resultToken"]

    evaluation = evaluate_compliance(configuration_item, rule_parameters)

    config = boto3.client("config")
    config.put_evaluations(
        Evaluations=[
            {
                "ComplianceResourceType":
                    configuration_item["resourceType"],
                "ComplianceResourceId":
                    configuration_item["resourceId"],
                "ComplianceType":
                    evaluation["compliance_type"],
                "Annotation":
                    evaluation["annotation"],
                "OrderingTimestamp":
                    configuration_item["configurationItemCaptureTime"]
            },
        ],
        ResultToken=result_token
    )
