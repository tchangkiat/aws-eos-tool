# Amazon EKS End-of-Support Tool

A data consolidation tool that provides insights of AWS EKS resources reaching end-of-support.

## Prerequisites

Install the following dependencies:

1. git
2. python
3. AWS CLI

## Setup

1. Clone this repository

2. Run the following commands to set up.

   - MacOS: `sh setup.sh`
   - Windows: `.\setup.bat`

3. Ensure that you have an existing / created a new IAM user with programmetic access. Generate an access key ID and secret access key for that user. The user should have the following permissions:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "eks-eos-tool",
      "Effect": "Allow",
      "Action": [
        "ec2:DescribeRegions",
        "eks:DescribeNodegroup",
        "eks:ListNodegroups",
        "eks:DescribeCluster",
        "eks:ListClusters"
      ],
      "Resource": "*"
    }
  ]
}
```

4. Replace the respective values in \<\> and run the commands to configure the AWS credentials:

```
aws configure set aws_access_key_id <access-key-id> --profile eks-eos

aws configure set aws_secret_access_key <secret-access-key> --profile eks-eos
```

## Usage

1. Run the following commands to activate virtualenv.

   - MacOS: `source eks-eos/bin/activate`
   - Windows: `eks-eos\Scripts\activate`

2. Run the tool using an account ID: `python eos.py`

3. The generated spreadsheets are located in the "output" folder.

### Running the tool for another AWS account

Re-configure the AWS credentials with the following commands, using the access key id and secret access key of an IAM user of that account. Subsequently, just re-run step #2 (or step #1-2 if the virtual environment was not activated).

```
aws configure set aws_access_key_id <access-key-id> --profile eks-eos

aws configure set aws_secret_access_key <secret-access-key> --profile eks-eos
```

### Retrieve metadata from selected regions

Add flag `-r <regions>`, where '\<regions\>' are comma-separated values of the regions. E.g. `python eos.py -r ap-southeast-1,us-east-1`

## Using The Data

- The "Update Health" column in the spreadsheet helps to prioritize the updates. These are the update health values:

  - `Green`: No action required.
  - `Yellow`: 4 months or less to plan and update.
  - `Red`: The version is out of support.

- You should update the EKS resources in "Red" health as soon as possible to avoid unplanned disruptions. The disruptions are caused by the auto-update that occurs anytime after the EOS dates. You may refer to the [Kubernetes Deprecation Guide](https://kubernetes.io/docs/reference/using-api/deprecation-guide/) to make the necessary changes when upgrading.

## Updating The Tool

1. Run the following commands to update.

   - MacOS: `sh update.sh`
   - Windows: `.\update.bat`

## References

1. [EKS v1.20 and above](https://docs.aws.amazon.com/eks/latest/userguide/kubernetes-versions.html#kubernetes-release-calendar)
2. [EKS v1.18 and v1.19](https://endoflife.date/amazon-eks)
