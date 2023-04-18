# End-of-Support Tool for AWS Resources

A data consolidation tool that provides insights of AWS resources reaching end-of-support.

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
      "Sid": "eos-tool",
      "Effect": "Allow",
      "Action": [
        "ec2:DescribeRegions",
        "eks:DescribeNodegroup",
        "eks:ListNodegroups",
        "eks:DescribeCluster",
        "eks:ListClusters",
        "rds:DescribeDBClusters",
        "rds:DescribeDBInstances"
      ],
      "Resource": "*"
    }
  ]
}
```

4. Replace the respective values in \<\> and run the commands to configure the AWS credentials:

```
aws configure set aws_access_key_id <access-key-id> --profile eos-tool

aws configure set aws_secret_access_key <secret-access-key> --profile eos-tool
```

## Usage

1. Run the following commands to activate virtualenv.

   - MacOS: `source eos-tool/bin/activate`
   - Windows: `eos-tool\Scripts\activate`

2. Run the tool using an account ID: `python eos.py`

3. The generated spreadsheets are located in the "output" folder.

### Running the tool for another AWS account

Re-configure the AWS credentials with the following commands, using the access key id and secret access key of an IAM user of that account. Subsequently, just re-run step #2 (or step #1-2 if the virtual environment was not activated).

```
aws configure set aws_access_key_id <access-key-id> --profile eos-tool

aws configure set aws_secret_access_key <secret-access-key> --profile eos-tool
```

### Retrieve metadata from selected regions

Add flag `-r <regions>`, where '\<regions\>' are comma-separated values of the regions. E.g. `python eos.py -r ap-southeast-1,us-east-1`

## Using The Data

- The "Update Health" column in the spreadsheet helps customers to prioritize the updates.

  - `Green`: More than 4 months to plan and update.
  - `Yellow`: 4 months or less to plan and update.
  - `Red`: The version is out of support.
  - `Unknown`: EOS date is not available.

- You should update the resources in `Red` health as soon as possible to avoid unplanned disruptions (caused by auto-update after EOS dates) and enjoy improved security posture, stability, and new features. Subsequently, you can plan ahead and update the resources in `Yellow` health.

## Updating The Tool

1. Run the following commands to update.

   - MacOS: `sh update.sh`
   - Windows: `.\update.bat`

## Supported Services

- Amazon EKS
- Amazon RDS
  - Supported engines: MariaDB, Microsoft SQL Server, MySQL, Oracle, PostgreSQL, Aurora (MySQL and PostgreSQL)
- Amazon Neptune

## References

1. [EKS v1.20 and above](https://docs.aws.amazon.com/eks/latest/userguide/kubernetes-versions.html#kubernetes-release-calendar)
2. [EKS v1.18 and v1.19](https://endoflife.date/amazon-eks)
3. [RDS - MariaDB](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/MariaDB.Concepts.VersionMgmt.html#MariaDB.Concepts.VersionMgmt.Supported)
4. [RDS - Microsoft SQL](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_SQLServer.html#SQLServer.Concepts.General.Deprecated-Versions)
5. [RDS - MySQL](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/MySQL.Concepts.VersionMgmt.html#MySQL.Concepts.VersionMgmt.Supported)
6. [RDS - Oracle](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_UpgradeDBInstance.Oracle.Overview.html#Aurora.VersionPolicy.MajorVersionLifetime)
7. [RDS - PostgreSQL](https://docs.aws.amazon.com/AmazonRDS/latest/PostgreSQLReleaseNotes/postgresql-release-calendar.html#PostgreSQL.Concepts.VersionMgmt.Supported)
8. [RDS - Aurora](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Aurora.VersionPolicy.html#Aurora.VersionPolicy.MajorVersionLifetime)
9. [Neptune](https://docs.aws.amazon.com/neptune/latest/userguide/engine-releases.html)
