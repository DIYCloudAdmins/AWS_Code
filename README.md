# AWS_Code

repo for AWS management code.  All code should be considered beta.

### Lambda Directory
code within the Lambda directory are designed to run via lambda without changes (though some are not designed to run directly, but via config or other means).

### Console Directory
code within the console directory are meant to be run directly from the python console.  They assume you have the AWS CLI installed and configured with an access_key and secret_key.  To configure run "aws configure" in the console and follow the prompts.

In longer scripts #region and #endregion tags are used to make sections collapsible. These tags are specific to the Visual Studio code dev environment.
