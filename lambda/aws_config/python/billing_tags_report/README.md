# BillingTagReport

creates an XLS file with the following tags (per ec2 resource): 
 InstanceID
 Name
 Owner
 Project
 Component
 Environment

creates an XLS file with the following tags (per ec2 resource): InstanceID Name Owner Project Component Environment

### To deploy
code requires the xksxwriter module to work. to install "pip install -t c:\local\directory\were\pyfile\is xlsxwriter"code requires the xksxwriter module to work. to install "pip install -t c:\local\directory\were\pyfile\is xlsxwriter"

This should be run locally assuming you also have boto3 and the AWS CLI installed.
