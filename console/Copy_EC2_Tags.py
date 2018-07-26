import boto3
#stolen and modified from: https://gist.github.com/mlapida/931c03cce1e9e43f147b
is_test = True
instances = boto3.resource('ec2').instances.all()

copyable_tag_keys = ["Name", "Application", "Project", "Component", "Environment", "Owner"]

for instance in instances:
    copyable_tags = [tags for tags in instance.tags if tags["Key"] in copyable_tag_keys] if instance.tags else []
    if not copyable_tags:
        continue

    # Tag the EBS Volumes
    print(f"{instance.instance_id}: {instance.tags}")
    for vol in instance.volumes.all():
        print(f"{vol.attachments[0]['Device']}: {copyable_tags}")
        if not is_test:
            vol.create_tags(Tags=copyable_tags)

    # Tag the Elastic Network Interfaces
    for eni in instance.network_interfaces:
        print(f"eth{str(eni.attachment['DeviceIndex'])}: {copyable_tags}")
        if not is_test:
            eni.create_tags(Tags=copyable_tags)