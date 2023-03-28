# EKS End-of-Support

A data consolidation tool that provides insights of AWS EKS resources reaching end-of-support.

## Prerequisites

1. AWS CLI
2. git
3. python

## Setup

1. Clone this repository

2. Run the following commands to set up.

   - MacOS: `sh setup.sh`
   - Windows: `.\setup.bat`

3. Run the following commands to activate virtualenv.

   - MacOS: `source eks-eos/bin/activate`
   - Windows: `eks-eos\Scripts\activate`

## Usage

1. Run the following commands to activate virtualenv.

   - MacOS: `source eks-eos/bin/activate`
   - Windows: `eks-eos\Scripts\activate`

2. Select one of the following options to run the tool.

   - Using payer account IDs: `python eos.py -p <payer account IDs>`
   - Using account IDs: `python eos.py -a <account IDs>`

   If you are using multiple account IDs, separate them by commas. E.g. `python eos.py -p 000000000000,111111111111`

3. The generated spreadsheets are located in the "output" folder.

### Retrieve metadata from selected regions

Add flag `-r <regions>`, where '\<regions\>' are comma-separated values of the regions. E.g. `python eos.py -p 000000000000 -r ap-southeast-1,us-east-1`

## Using The Data

- The "Update Health" column in the spreadsheet helps to prioritize the updates. These are the update health values:

  - `Green`: No action required.
  - `Yellow`: 4 months or less to plan and update.
  - `Red`: The version is out of support.
  - `Unknown`: EOS date is not available.

- You can filter by 'Red' and highlight the need to update those resources promptly.

- If the EOS dates are "Not available", they are not released in the official documentations yet (see [References](#references)).

## Updating The Tool

1. Run the following commands to update.

   - MacOS: `sh update.sh`
   - Windows: `.\update.bat`

## References

1. [EKS v1.20 and above](https://docs.aws.amazon.com/eks/latest/userguide/kubernetes-versions.html#kubernetes-release-calendar)
2. [EKS v1.18 and v1.19](https://endoflife.date/amazon-eks)
