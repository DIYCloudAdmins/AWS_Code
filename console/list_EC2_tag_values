import boto3
import xlsxwriter
#requires the boto3 and xlsxwriter packages to run.
#pip install packageName

workbook = xlsxwriter.Workbook("Tag_Report.xlsx")
worksheet = workbook.add_worksheet("Tags")

client=boto3.client("ec2")
response=client.describe_instances()
ec2inst=boto3.resource("ec2")

x = 0
instanceList = []
for reservation in response["Reservations"]:
    for instance in reservation["Instances"]:
        instanceID = instance["InstanceId"]
        EC2instance = ec2inst.Instance(instanceID)
        returnMSG = ""
        instancePass = True

        taglist = {}
        currDict ={}
        currDict["InstanceID"] = instanceID
        for tagPairs in EC2instance.tags:
            currDict[tagPairs["Key"]] = tagPairs["Value"]
        instanceList.append(currDict)

#write headers to the worksheet
worksheet.write(0,0,"InstanceID")
worksheet.write(0,1,"InstanceName")
worksheet.write(0,2,"Owner")
worksheet.write(0,3,"Project")
worksheet.write(0,4,"Component")
worksheet.write(0,5,"Environment")

row = 1
col = 0
#one section for each header.
for inst in instanceList:
    if "InstanceID" in inst:
        worksheet.write(row, col,inst["InstanceID"])
        col +=1
    else:
        worksheet.write(row, col,"")
        col +=1
    if "Name" in inst:
        worksheet.write(row, col,inst["Name"])
        col +=1
    else:
        worksheet.write(row, col,"")
        col +=1
    if "Owner" in inst:
        worksheet.write(row, col,inst["Owner"])
        col +=1
    else:
        worksheet.write(row, col,"")
        col +=1
    if "Project" in inst:
        worksheet.write(row, col,inst["Project"])
        col +=1
    else:
        worksheet.write(row, col,"")
        col +=1
    if "Component" in inst:
        worksheet.write(row, col,inst["Component"])
        col +=1
    else:
        worksheet.write(row, col,"")
        col +=1
    if "Environment" in inst:
        worksheet.write(row, col,inst["Environment"])
        col +=1
    else:
        worksheet.write(row, col,"")
        col +=1
    row += 1
    col = 0

