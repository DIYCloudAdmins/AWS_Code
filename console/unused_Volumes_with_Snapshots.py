import boto3
   
ec2 = boto3.resource('ec2')

print("Created,AZ,VolumeID,VolumeType,State,Size,IOPs,SnapshotID")
x = 0

volumes = ec2.volumes.all() # If you want to list out all volumes
volumes = ec2.volumes.filter(Filters=[{'Name': 'status', 'Values': ['available']}]) 
for volume in volumes:
    currentVolume = ec2.Volume(volume.id)
    if currentVolume.snapshot_id != "":
        print(str(currentVolume.create_time) + "," + currentVolume.availability_zone + "," + currentVolume.volume_id + "," + currentVolume.volume_type + "," + currentVolume.state + "," + str(currentVolume.size) + "," + str(currentVolume.iops) + "," + currentVolume.snapshot_id)
