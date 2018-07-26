import boto3
import xlsxwriter

#create excel file to write report to
workbook = xlsxwriter.Workbook("Audit_Report.xlsx")

#Standard variables I might want to use
vpcIDs = [{"Name":"VPC-Apps-E1-01","ID":"vpc-7676eb0d"},{"Name":"VPC-INFRA-E1-01","ID":"vpc-336cf148"},{"Name":"AppsDev_Legacy_10.4.0.0/16","ID":"vpc-a859a8c6"}]
regionName = "us-east-1"
accountID = "xxxxxxxxxxxxxxx"


#-------------------------------Does the actual work of writing to excel.  output argument is in the form of a list, wrkSheet is a sheet object------
def writeToExcel(output, wrkSheet, rowCount):
    col = 0
    row = rowCount

    for items in output:
#        print(items)
        wrkSheet.write(row,col,items)
        col += 1
    return rowCount

#-----------------------------------------------------------------------------------------------------------------------------------
#region
#--------------------Creates a Legend Sheet for the xlxs report-------------------------

#legend sheet workbook and global variables.
legendSheet = workbook.add_worksheet("Legend")
legendSheetRow = 0

def createLegend():
    global legendSheetRow
    writeToExcel(["Sheet","","Explination"],legendSheet,legendSheetRow)
    legendSheetRow +=1
    writeToExcel(["Tag Audit","","Lists all EC2 instances in the Main account, the header row indicates required tags, blanc cells in a row indicate a missing tag"],legendSheet,legendSheetRow)
    legendSheetRow +=1
    writeToExcel(["Egress Open","","Lists all Security Groups that have open access (all ports to 0.0.0.0/0).  Ports should be specific to need and not open all all internet addresses"],legendSheet,legendSheetRow)
    legendSheetRow +=1
    writeToExcel(["Unused Groups","","List of groups that are not currently attached to a resource"],legendSheet,legendSheetRow)
    legendSheetRow +=1
    writeToExcel(["RDS Tags","","List of RDS Databases and their Tags"],legendSheet,legendSheetRow)
    legendSheetRow +=1
    writeToExcel(["Unused Volumes","","List of unused volumes that have snapshots associated"],legendSheet,legendSheetRow)


#-----------------------------------------------------------------------------------------------------
#endregion
#region
#---------------------Logs EC2 Tags to the xlxs report------------------------------------------------


EC2tagsSheet = workbook.add_worksheet("EC2 Tag Audit")
EC2tagsSheetRow = 0

def EC2tagLogs():
    client=boto3.client("ec2")
    response=client.describe_instances()
    ec2inst=boto3.resource("ec2")
    instanceList = []
    global EC2tagsSheetRow

    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            instanceID = instance["InstanceId"]
            EC2instance = ec2inst.Instance(instanceID)
            returnMSG = ""
            instancePass = True
            taglist = {}
            currDict ={}
            currDict["InstanceID"] = instanceID
            try:
                for tagPairs in EC2instance.tags:
                    currDict[tagPairs["Key"]] = tagPairs["Value"]
                instanceList.append(currDict)
            except:
                #come back and add default values for instances with 0 tags
                p = 0
    # write header row to excel
    writeToExcel(["InstanceID","InstanceName","Owner","Project","Component","Environment"],EC2tagsSheet,0)
    EC2tagsSheetRow +=1
    tagsLst = []
    for inst in instanceList:
        if "InstanceID" in inst:
            tagsLst.append(inst["InstanceID"])
        else:
            tagsLst.append("")
        if "Name" in inst:
            tagsLst.append(inst["Name"])
        else:
            tagsLst.append("")
        if "Owner" in inst:
            tagsLst.append(inst["Owner"])
        else:
            tagsLst.append("")
        if "Project" in inst:
            tagsLst.append(inst["Project"])
        else:
            tagsLst.append("")
        if "Component" in inst:
            tagsLst.append(inst["Component"])
        else:
            tagsLst.append("")
        if "Environment" in inst:
            tagsLst.append(inst["Environment"])
        else:
            tagsLst.append("")
        #write one row of EC2 Tags
        writeToExcel(tagsLst,EC2tagsSheet,EC2tagsSheetRow) 
        EC2tagsSheetRow +=1
        tagsLst.clear()
       
#------------------------------------------------------------------------------------------------------
#endregion
#region
#---------------------Lists all security groups that are not attached to an EC2 instance --------------

#global variables and objects for unusedSecurityGroups()
unusedGroupSheet = workbook.add_worksheet("UnusedGroups")
unusedGroupSheetRow=0

def unusedSecurityGroups():
    global unusedGroupSheetRow
    ec2 = boto3.resource('ec2')
    sgs = ec2.security_groups.all() # Fetching all security groups in AWS account
    all_sgs = set([sg.group_name for sg in sgs]) # Creating a list of only security group names
    instances = ec2.instances.all() # Getting all instances in AWS account
    inssgs = set([sg['GroupName'] for ins in instances for sg in ins.security_groups]) # Getting all security groups attached to any instances
    unused_sgs = all_sgs - inssgs # Removing duplicate SGs
    writeToExcel(["Unused Group"],unusedGroupSheet,unusedGroupSheetRow)
    unusedGroupSheetRow +=1
    for sg in unused_sgs:
        writeToExcel([sg],unusedGroupSheet,unusedGroupSheetRow)
        unusedGroupSheetRow +=1

#------------------------------------------------------------------------------------------------------
#endregion
#region
#------------------------Lists all security groups with egress with ip range 0.0.0.0/0-----------------
#global objects and variables of openSecurityGroups()
openEgressSGSheet = workbook.add_worksheet("Egress Open")
openEgressSGSheetRow=0


def openSecurityGroups():
    global openEgressSGSheetRow
    ec2 = boto3.client('ec2')
    # create header row
    writeToExcel(["VPC","VPCName","GroupName","GroupID"],openEgressSGSheet,openEgressSGSheetRow)
    openEgressSGSheetRow +=1
    for vpcs in vpcIDs:
        response = ec2.describe_security_groups(
            Filters=[
                {
                    "Name":"vpc-id", "Values":[vpcs["ID"]]
                }
            ]
        )
        for groups in response['SecurityGroups']:
            for addresses in groups['IpPermissionsEgress']:
                for address in addresses['IpRanges']:
                    if address['CidrIp'] == "0.0.0.0/0":
                        writerow =(vpcs["ID"],vpcs["Name"],groups["GroupName"],groups["GroupId"])
                        writeToExcel(writerow,openEgressSGSheet,openEgressSGSheetRow) 
                        openEgressSGSheetRow +=1

#----------------------------------------------------------------------------------------------
#endregion
#region
#-----------------------List Tags Associated with RDS instances--------------------------------

# Global variables, function,  and helper functions for RDStagLogs
rdsList=[]
rdsDict = {}
rdsTagSheet = workbook.add_worksheet("RDS Tags")
rdsTagSheetRow=0

def buildRDSlist(dictionary):
    global rdsList
    localdict={}
    for x,y in dictionary.items():
        localdict[x]=y
    rdsList.append(localdict)

def RDStagsLogs():
    global rdsTagSheetRow
    global rdsList
    global rdsDict        
    rds = boto3.client("rds")
    writerow = []
    ResourceName="arn:aws:rds:" + regionName + ":" + accountID + ":db:"
    
    #write header row to sheet
    writeToExcel(["Name","Project","Component","Owner","Environment"],rdsTagSheet,rdsTagSheetRow)
    rdsTagSheetRow +=1

    rds_client = boto3.client('rds', 'us-east-1')
    db_instance_info = rds_client.describe_db_instances()

    #print(db_instance_info)
    for each_db in db_instance_info['DBInstances']:
        rdsDict["DBName"] = each_db['DBInstanceIdentifier']
        response = rds_client.list_tags_for_resource(
        ResourceName=each_db['DBInstanceArn'])
        for n in response["TagList"]:
            # print(n["Key"])
            # print(n["Value"])
            rdsDict[n["Key"]] = n["Value"]
        buildRDSlist(rdsDict)
        rdsDict.clear()

    for records in rdsList:
        for key,value in records.items():
            if key == "DBName":
                writerow.append(records[key])
            else:
                writerow.append("")
            if key == "Project":
                writerow.append(records[key])
            else:
                writerow.append("")
            if key =="Component":
                writerow.append(records[key])
            else:
                writerow.append("")
            if key == "Owner":
                writerow.append(records[key])
            else:
                writerow.append("")
            if key == "Environment":
                writerow.append(records[key])
            else:
                writerow.append("")
            writeToExcel(writerow,rdsTagSheet,rdsTagSheetRow)
            writerow.clear()
        rdsTagSheetRow +=1

#------------------------------------------------------------------------------------
#endregion
#region
#----------------------------logs unused volumes that have a snapshot----------------
unusedVolumeTagSheet = workbook.add_worksheet("Unused Volumes")
UnusedVolumeTagSheetRow=0  

def unusedVolumes():
    ec2 = boto3.resource('ec2')
    global unusedVolumeTagSheet
    global UnusedVolumeTagSheetRow
    writeToExcel(["Created","AZ","VolumeID","VolumeType","State","Size","IOPs","SnapshotID"],unusedVolumeTagSheet,UnusedVolumeTagSheetRow)
    UnusedVolumeTagSheetRow += 1

    volumes = ec2.volumes.filter(Filters=[{'Name': 'status', 'Values': ['available']}]) 
    for volume in volumes:
        volumeAttributes = ec2.Volume(volume.id)
        if volumeAttributes.snapshot_id != "":
            writeToExcel([str(volumeAttributes.create_time),volumeAttributes.availability_zone,volumeAttributes.volume_id,volumeAttributes.volume_type,volumeAttributes.state,volumeAttributes.size,volumeAttributes.iops,volumeAttributes.snapshot_id],unusedVolumeTagSheet,UnusedVolumeTagSheetRow)
            UnusedVolumeTagSheetRow += 1



#------------------------------------------------------------------------------------
#endregion
# ------------------------Calls all the functions------------------------------------
createLegend()
EC2tagLogs()
openSecurityGroups()
unusedSecurityGroups()
RDStagsLogs()
unusedVolumes()
workbook.close()

#end
