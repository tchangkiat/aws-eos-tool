# Amazon EKS End-of-Support Tool

A data consolidation tool that provides insights of AWS EKS resources reaching end-of-support.

## Prerequisites

Install the following dependencies:

1. git
2. python
3. AWS CLI - Need to [set up a default credential using access key ID and secret access key](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-creds)

## Setup

1. Clone this repository

2. Run the following commands to set up.

   - MacOS: `sh setup.sh`
   - Windows: `.\setup.bat`

## Usage

1. Run the following commands to activate virtualenv.

   - MacOS: `source eks-eos/bin/activate`
   - Windows: `eks-eos\Scripts\activate`

2. Run the tool using an account ID: `python eos.py`

3. The generated spreadsheets are located in the "output" folder.

### Retrieve metadata from selected regions

Add flag `-r <regions>`, where '\<regions\>' are comma-separated values of the regions. E.g. `python eos.py -r ap-southeast-1,us-east-1`

## Using The Data

- The "Update Health" column in the spreadsheet helps to prioritize the updates. These are the update health values:

  - `Green`: No action required.
  - `Yellow`: 4 months or less to plan and update.
  - `Red`: The version is out of support.
  - `Unknown`: EOS date is not available.

- The resources in "Red" health should be updated as soon as possible to avoid unplanned disruptions. The disruptions are caused by the auto-update that occurs anytime after the EOS dates.

## Updating The Tool

1. Run the following commands to update.

   - MacOS: `sh update.sh`
   - Windows: `.\update.bat`

## References

1. [EKS v1.20 and above](https://docs.aws.amazon.com/eks/latest/userguide/kubernetes-versions.html#kubernetes-release-calendar)
2. [EKS v1.18 and v1.19](https://endoflife.date/amazon-eks)
