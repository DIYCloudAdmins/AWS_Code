import boto3

def buildRDSlist(dictionary):
    global rdsList
    localdict={}
    for x,y in dictionary.items():
        localdict[x]=y
    rdsList.append(localdict)



rds = boto3.client("rds")
rds_client = boto3.client('rds', 'us-east-1')
db_instance_info = rds_client.describe_db_instances()
rdsList = []
rdsDict = {}


# ResourceName="arn:aws:rds:" + regionName + ":" + accountID + ":db:"

for each_db in db_instance_info['DBInstances']:
        rdsDict["DBName"] = each_db['DBInstanceIdentifier']
        response = rds_client.list_tags_for_resource(
        ResourceName=each_db['DBInstanceArn'])
        for n in response["TagList"]:  #no need to rebuilt the dictionary...needs to be updated.
            rdsDict[n["Key"]] = n["Value"]
        buildRDSlist(rdsDict)
        rdsDict.clear()

for records in rdsList:
    print(records)
