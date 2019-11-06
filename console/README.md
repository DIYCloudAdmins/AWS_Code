# Script Descriptions

### AWS_Audit_Resources.py
Master script, creates an xlsx file with output from the other scripts in this directory.  Requires the Boto3 and xlsxwriter packages (get them from pip).

### list_EC2_tag_values.py
Lists specific EC2 tag values writes them to an xlsx file.  To add/delete tags change the if statements at the bottom of the script.

### list_RDS_Tags
Prints specific tags related to RDS instances.  To add/delete tags change the if statements at the bottom of the script.

### list_SecurityGroups_Outbound_Open.py
Prints all security groups with an egress rule containing an IP range of 0.0.0.0/0
I added a filter block to the bottom (commented out) to remember how to restrict to specific VPCs)

### list_SecurityGroup_Rules.py
Prints all security group rules with ingress and egress rules.

### Unused_Volumes_with_Snapshots.py
Prints all volumes that are unattached and that have a snapshot associated with them.

### ec2_noProjectTags.py
idetifies all ec2 instances without a project tag:
    1. emails warning after specified time
    2. terminates instances after alternative specified time