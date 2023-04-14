from argparse import ArgumentParser
from pathlib import Path
from datetime import date
from concurrent.futures import ThreadPoolExecutor
from functools import partial
import os
import sys
import logging
import datetime
import time
import json
import boto3
import pandas as pd
import traceback

config = json.load(open("config.json"))
eos = json.load(open("eos.json"))

try:
    os.remove("error.log")
except OSError:
    pass

logger = logging.getLogger("default")
logger.setLevel(logging.INFO)
logger.propagate = False
sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
formatter = logging.Formatter('%(message)s')
sh.setFormatter(formatter)
logger.addHandler(sh)

err_logger = logging.getLogger("error")
err_logger.setLevel(logging.ERROR)
err_logger.propagate = False
fh = logging.FileHandler("error.log")
fh.setLevel(logging.ERROR)
formatter = logging.Formatter('[%(asctime)s] %(message)s', '%Y-%m-%d %H:%M:%S')
fh.setFormatter(formatter)
err_logger.addHandler(fh)

session = boto3.Session(profile_name="eos-tool")

def main(args=None):
    # Clear the console screen
    if "win32" in sys.platform:
        _ = os.system("cls")
    else:
        _ = os.system("clear") 

    parser = ArgumentParser(description="Amazon EKS End-of-Support (EOS) Tool")
    parser.add_argument("-r", "--regions", help="Comma-separated list of regions", nargs="?", dest="regions", default=None)
    args = parser.parse_args(args)

    sts = session.client('sts')
    sts.get_caller_identity()["Account"]
    account = sts.get_caller_identity()["Account"]

    regions = []
    if args.regions:
        r = args.regions.split(",")
        if len(r) > 0:
            regions = r
    else:
        ec2 = session.client("ec2", region_name="us-east-1")
        regions = [r["RegionName"] for r in ec2.describe_regions(AllRegions=False)["Regions"]]

    consolidate_data(account, [account], regions)
    logger.info("")

# --------------------
# Functions - General
# --------------------

def consolidate_data(name, accounts, regions):
    start_time = time.time() # Track time elapsed

    output_file_path = "output/EOS-" + name + ".xlsx"
    df = pd.DataFrame({
        "Account": [],
        "Service": [],
        "Resource Type": [],
        "Resource Name": [],
        "Regions / AZs": [],
        "Group": [],
        "Update Health": [],
        "Engine": [],
        "Version": [],
        "End-of-Support": [],
        "Insights": []
    })
    
    with ThreadPoolExecutor() as executor:
        executor.map(partial(consolidate_data_by_account, df, regions), accounts)
    
    # --------------------------------------------------------------------------------
    # Storing data in an Excel spreadsheet
    # --------------------------------------------------------------------------------
    Path("output").mkdir(parents=True, exist_ok=True)
    df.sort_values(['Group', 'Resource Type'],ascending = [True, True])
    df.reset_index(drop=True).style.applymap(highlight_update_health, subset=["Update Health"]).to_excel(output_file_path, sheet_name=datetime.datetime.now().strftime("%Y%m%d.%H%M"), index=False)
    end_time = time.time()

    logger.info("-")
    logger.info("Elapsed Time: " + str(round(end_time - start_time, 2)) + " seconds")
    logger.info("Result: '" + output_file_path + "'")
    logger.info("--------------------------------------------------")
    logger.info("")

def consolidate_data_by_account(dataframe, regions, account):
    with ThreadPoolExecutor() as executor:
        executor.map(partial(consolidate_data_by_region, dataframe, account), regions)
        
def consolidate_data_by_region(dataframe, account, region):
    try:
        eks_populate_cluster_details(account, region, dataframe)
    except Exception as e:
        logger.error("<" + e.__class__.__name__ + "> " + e.args[0])
        err_logger.error(traceback.format_exc())

def days_to_eos(eos_date_str):
    eos_date = format_date(eos_date_str, False)
    if eos_date != "Not available":
        today = date.today()
        return (eos_date - today).days
    return None

def evaluate_eos(str_date, service = ""):
    red_message = "Out of support."
    yellow_message = ""

    if service == "lambda":
        red_message += " Update this resource to enjoy improved security posture, stability, and new features."
        yellow_message = " Update this resource before the EOS date to enjoy improved security posture, stability, and new features."
    else:
        red_message += " Update this resource to avoid unplanned disruption, and enjoy improved security posture, stability, and new features."
        yellow_message = " Update this resource to avoid unplanned disruption after the EOS date, and enjoy improved security posture, stability, and new features."

    if str_date == "EOS":
        return {"updateHealth": "Red", "message": red_message}

    days = days_to_eos(str_date)
    
    if days is None:
        return { "updateHealth": "Unknown", "message": "EOS date is not available." }
    
    if days >= 0:
        message = "EOS in {} days.".format(days)
        if days <= 122:
            return {"updateHealth": "Yellow", "message": message + yellow_message}
        else:
            return {"updateHealth": "Green", "message": message + " No action required."}
    else:
        return {"updateHealth": "Red", "message": red_message}
    
def format_date(str_date, str_format=True):
    date_segments = str_date.split("/")
    month = config["month"]
    if len(date_segments) == 2:
        if str_format == True:
            return month[int(date_segments[0])-1] + " " + date_segments[1]
        else: 
            return date(int(date_segments[1]), int(date_segments[0]), 1)
    elif len(date_segments) == 3:
        if str_format == True:
            return date_segments[0] + " " + month[int(date_segments[1])-1] + " " + date_segments[2]
        else:
            return date(int(date_segments[2]), int(date_segments[1]), int(date_segments[0]))
    else:
        return str_date

def add_data(dataframe, account, service, resource_type, resource_name, regions_azs, group, updateHealth, engine, version, eos, insights):
    dataframe.loc[len(dataframe.index)] = [account, service, resource_type, resource_name, regions_azs, group, updateHealth, engine, version, eos, insights]

def highlight_update_health(val):
    color = "transparent"
    if val == "Red":
        color = "#ffc2d1"
    elif val == "Yellow":
        color = "#fcf5c7"
    elif val == "Green":
        color = "#9bd0b7"
    return 'background-color: {}'.format(color)

# --------------------
# Functions - EKS
# --------------------

def eks_get_eos_date(version):
    eks_eos = eos["eks"]
    for rec in eks_eos:
        if rec["version"] == version:
            return rec["eos"]
    return "Not available"

def eks_populate_cluster_details(account, region, dataframe):
    eks = session.client('eks', region_name=region)

    clusters = eks.list_clusters()["clusters"]
    logger.info("Retrieving EKS resources for "  + account + " in " + region)

    for cluster in clusters:
        # Populate cluster details
        cluster_details = eks.describe_cluster(name=cluster)["cluster"]

        cluster_region = cluster_details["arn"].split(":")[3]
        cluster_insights = []
        cluster_version_eos_date_str = eks_get_eos_date(cluster_details["version"])
        evaluation_result = evaluate_eos(cluster_version_eos_date_str, cluster_details["version"])
        cluster_insights.append(evaluation_result["message"])
        add_data(dataframe, account, "EKS", "Cluster", cluster_details["name"], cluster_region, cluster_details["name"], evaluation_result["updateHealth"], "Kubernetes", cluster_details["version"], format_date(cluster_version_eos_date_str), " ".join(cluster_insights))

        # Populate nodegroup details
        eks_populate_nodegroup_details(eks, cluster_details, account, dataframe)


def eks_populate_nodegroup_details(eks, cluster_details, account_id_name, dataframe):
    nodegroups = eks.list_nodegroups(clusterName=cluster_details["name"])["nodegroups"]
    for nodegroup in nodegroups:
        nodegroup_details = eks.describe_nodegroup(clusterName=cluster_details["name"], nodegroupName=nodegroup)["nodegroup"]
        nodegroup_insights = []
        nodegroup_version_eos_date_str = eks_get_eos_date(nodegroup_details["version"])
        evaluation_result = evaluate_eos(nodegroup_version_eos_date_str, nodegroup_details["version"])
        nodegroup_insights.append(evaluation_result["message"])
        if nodegroup_details["version"] != cluster_details["version"]:
            nodegroup_insights.append("Nodegroup version ({}) should match cluster version ({}) to avoid compatibility issues.".format(nodegroup_details["version"], cluster_details["version"]))
            evaluation_result["updateHealth"] = "Red"
        add_data(dataframe, account_id_name, "EKS", "Nodegroup", nodegroup_details["nodegroupName"], cluster_details["arn"].split(":")[3], nodegroup_details["clusterName"], evaluation_result["updateHealth"], "Kubernetes", nodegroup_details["version"], format_date(nodegroup_version_eos_date_str), " ".join(nodegroup_insights))


########################################################################################

if __name__ == '__main__':
    main()