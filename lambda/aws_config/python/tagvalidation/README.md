# validate_tags_main_vpcs.py

original code from the [awslabs aws-config-rules repo](https://github.com/awslabs/aws-config-rules/blob/master/python/ec2_require_tags_with_valid_values.py)
from the original I added timing code, instances without all proper tags will be allowed from 0 to 4 hours, from 4 - 10 hours they will be reported, from 10 hours to 5 days they will be stopped (every time even if they are restarte), and after 10 days they will be terminated.

Script relies on python-dateutil.  to install this package "pip install -t "c:\directory\structure\where\script\exists" dateutil

Within the script there is line that filters VPCs "if instance.vpc_id == "vpc-a859a8c6":"  change this line (or delete the clause) to filter on different VPCs

To depoly edit script as needed rename the Validate_tags.py* to lambda_function.py and zip that file and the dateutil directory into a zip file and upload to a lambda function.

### This function needs a config rule to function.
The config rule resource type should be: EC2 Instance
Config rule parameters are the key and values you would like to test for.
Key:Name Value:* will ensure the name tag is applied (any value is valid)
Key:Department Value:IT,Sale,Engineering will ensure the Dapartment tag is applied and only be considered valide if IT,Sales, or Engineering are in the Value field.



*it is possible to change the lambda handler name instead of the file name, to me this is not prefered.
