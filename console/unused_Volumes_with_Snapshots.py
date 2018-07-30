import boto3
import xlsxwriter
#requires the boto3 and xlsxwriter packages to run.
#pip install packageName

workbook = xlsxwriter.Workbook("volumeDeletion.xlsx")
worksheet = workbook.add_worksheet("Volumes")
   
ec2 = boto3.resource('ec2')

testing = True

print("Created,AZ,VolumeID,VolumeType,State,Size,IOPs,SnapshotID")
x = 0

# volumes = ec2.volumes.all() # If you want to list out all volumes
volumes = ec2.volumes.filter(Filters=[{'Name': 'status', 'Values': ['available']}]) 
for volume in volumes:
    currentVolume = ec2.Volume(volume.id)
    if currentVolume.snapshot_id != "":
        print(str(currentVolume.create_time) + "," + currentVolume.availability_zone + "," + currentVolume.volume_id + "," + currentVolume.volume_type + "," + currentVolume.state + "," + str(currentVolume.size) + "," + str(currentVolume.iops) + "," + currentVolume.snapshot_id)
        worksheet.write(x,0,str(currentVolume.create_time))
        worksheet.write(x,1,currentVolume.availability_zone)
        worksheet.write(x,2,currentVolume.volume_id)
        worksheet.write(x,3,currentVolume.volume_type)
        worksheet.write(x,4,currentVolume.state)
        worksheet.write(x,5,str(currentVolume.size))
        worksheet.write(x,6,str(currentVolume.iops))
        worksheet.write(x,7,currentVolume.snapshot_id)
        x += 1
    if testing == False:
        currentVolume.delete()
    
