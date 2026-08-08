#list ec2 instances
from langchain.tools import tool
import sys
import boto3
import json

ec2 = boto3.client('ec2')
key_pair="proj-key"
security_group="sg-031e6b3d2d272267b"

AMI_FILTERS = {
    "amazon-linux": {
        "owner": "amazon",
        "name": "al2023-ami-*"
    },
    "ubuntu": {
        "owner": "099720109477",
        "name": "ubuntu/images/hvm-ssd-gp3/ubuntu-noble-24.04-amd64-server-*"
    },
    "debian": {
        "owner": "136693071363",
        "name": "debian-12-amd64-*"
    },
    "rhel": {
        "owner": "309956199498",
        "name": "RHEL-9.*x86_64*"
    },
    "windows": {
        "owner": "amazon",
        "name": "Windows_Server-2022-English-Full-Base-*"
    },
    "macos": {
        "owner": "amazon",
        "name": "amzn-ec2-macos-*"
    }
}

@tool
def list_instances():
    """lists all the instances"""
    all_instances=[]
    response = ec2.describe_instances()
    for reservations in response['Reservations']:
        for instance in reservations['Instances']:
            all_instances.append({
                "id": instance["InstanceId"],
                "state": instance["State"]["Name"],
                "tags": instance.get("Tags", []),
                "ip": instance.get("PublicIpAddress", "No Public IP Address"),
                "ami_id": instance["ImageId"],
                "instance_type": instance["InstanceType"],
                "launch_time": instance["LaunchTime"]
            })
    if len(all_instances)==0:
        return "No EC2 instances found in your AWS account or region."
    return all_instances

@tool
def describe_instance(instance_id):
    """describes an instance by id"""
    try:
        response = ec2.describe_instances(
            InstanceIds=[
                instance_id,
            ],
        )
        return json.dumps({
            "status": True,
            "message": "Instance described",
            "instance_id": instance_id,
            "aws_response": response
        })
    except Exception as e:
        return json.dumps({
            "status": False,
            "message": "error describing instance",
            "error_type": type(e).__name__,
            "error": str(e)
        })


@tool
def get_instance_by_id(instance_id):
    """gets the instance by id"""
    response = ec2.describe_instances()
    for reservations in response['Reservations']:
        for instance in reservations['Instances']:
            if instance_id==instance['InstanceId']:
                return instance['InstanceId']
    return "instance not found"

def get_instance_by_id_helper(instance_id):
    """gets the instance by id as a helper function for a tool"""
    response = ec2.describe_instances()
    for reservations in response['Reservations']:
        for instance in reservations['Instances']:
            if instance_id==instance['InstanceId']:
                return instance['InstanceId'],instance['State']
    return "instance not found","not found"

@tool
def start_instance(instance_id):
    """starts an existing instance by id"""
    instance_id,state = get_instance_b_id(instance_id)

    #instance not found
    if instance_id == "instance not found" and state == "not found":
        return "instance not found"
    
    #instance is terminated
    if state["Code"] == 48:
        return "the instance is terminated, cannot restart it"
    
    #instance is running
    if state["Code"] == 16:
        return "the instance is already running"
    
    #instance is pending
    elif state["Code"] == 0:
        return "the instance is pending"
    
    #instance is Stopping
    elif state["Code"] == 64:
        return "the instance is stopping, wait until it becomes stopped."

    #instance is Shutting down
    elif state["Code"] == 20:
        return "the instance is shutting down"
    
    #instance is stopped
    elif state["Code"] == 80:
        try:
            response = ec2.start_instances(
                InstanceIds=[
                    instance_id,
                ],
            )
            return json.dumps({
                "status": True,
                "message": "Instance is starting",
                "instance_id": instance_id,
                "state": "starting",
                "aws_response": response
            })
        except Exception as e:
            return json.dumps({
                "status": False,
                "message": "error starting instance",
                "error_type": type(e).__name__,
                "error": str(e)
            })
    else:
        return json.dumps({
            "status": False,
            "message": "instance not found",
            "error_type": "InstanceNotFound",
            "instance_id": instance_id
        })

@tool
def stop_instance(instance_id):
    """stops an existing running instance by id"""
    instance_id,state = get_instance_b_id(instance_id)

    #instance not found
    if instance_id == "instance not found" and state == "not found":
        return "instance not found"
    
    #instance is terminated
    if state["Code"] == 48:
        return "the instance is terminated, cannot restart it"
    
    #instance is running
    if state["Code"] == 16:
        try:
            response = ec2.stop_instances(
                InstanceIds=[
                    instance_id,
                ],
            )
            return json.dumps({
                "status": True,
                "message": "Instance is stopping",
                "instance_id": instance_id,
                "state": "stopping",
                "aws_response": response
            })

        except Exception as e:
            return json.dumps({
                "status": False,
                "message": "error stopping instance",
                "error_type": type(e).__name__,
                "error": str(e)
            })
    
    #instance is pending
    elif state["Code"] == 0:
        return "the instance is pending"
    
    #instance is Stopping
    elif state["Code"] == 64:
        return "the instance is stopping, wait until it becomes stopped."

    #instance is Shutting down
    elif state["Code"] == 20:
        return "the instance is shutting down"
    
    #instance is stopped
    elif state["Code"] == 80:
        return "the instance is already stopped"
    else:
        return "instance not found"

@tool
def restart_instance(instance_id):
    """restarts an existing instance by id"""
    instance_id,state = get_instance_b_id(instance_id)

    #instance not found
    if instance_id == "instance not found" and state == "not found":
        return "instance not found"
    
    #instance is terminated
    if state["Code"] == 48:
        return "the instance is terminated, cannot restart it"
    
    #instance is running
    if state["Code"] == 16:
        try:
            response = ec2.reboot_instances(
                InstanceIds=[
                    instance_id,
                ],
            )
            return json.dumps({
                "status": True,
                "message": "Instance is restarting",
                "instance_id": instance_id,
                "state": "restarting",
                "aws_response": response
            })
        except Exception as e:
            return json.dumps({
                "status": False,
                "message": "error restarting instance",
                "error_type": type(e).__name__,
                "error": str(e)
            })
    
    #instance is pending
    elif state["Code"] == 0:
        return "the instance is pending"
    
    #instance is Stopping
    elif state["Code"] == 64:
        return "the instance is stopping, wait until it becomes stopped."

    #instance is Shutting down
    elif state["Code"] == 20:
        return "the instance is shutting down"
    
    #instance is stopped
    elif state["Code"] == 80:
        return "the instance is stopped"
    else:
        return "instance not found"

@tool
def terminating_instance(instance_id):
    """terminate an existing instance by id"""
    instance_id,state = get_instance_b_id(instance_id)

    #instance not found
    if instance_id == "instance not found" and state == "not found":
        return "instance not found"
    
    #instance is terminated
    if state["Code"] == 48:
        return "the instance is terminated, cannot restart it"
    
    #instance is running
    if state["Code"] == 16:
        try:
            response = ec2.terminate_instances(
                InstanceIds=[
                    instance_id,
                ],
            )
            return json.dumps({
                "status": True,
                "message": "Instance is terminating",
                "instance_id": instance_id,
                "state": "terminating",
                "aws_response": response
            })
        except Exception as e:
            return json.dumps({
                "status": False,
                "message": "error terminating instance",
                "error_type": type(e).__name__,
                "error": str(e)
            })
    
    #instance is pending
    elif state["Code"] == 0:
        return "the instance is pending, wait until running"
    
    #instance is Stopping
    elif state["Code"] == 64:
        return "the instance is stopping, wait until it becomes stopped."

    #instance is Shutting down
    elif state["Code"] == 20:
        return "the instance is shutting down"
    
    #instance is stopped
    elif state["Code"] == 80:
        try:
            response = ec2.terminate_instances(
                InstanceIds=[
                    instance_id,
                ],
            )
            return json.dumps({
                "status": True,
                "message": "Instance is terminating",
                "instance_id": instance_id,
                "state": "terminating",
                "aws_response": response
            })
        except Exception as e:
            return json.dumps({
                "status": False,
                "message": "error terminating instance",
                "error_type": type(e).__name__,
                "error": str(e)
            })

    else:
        return "instance not found"

@tool
def create_instance(os: str,name: str,instance_type: str, disk_size: int):
    """create a new EC2 instance"""
    try:
        response = ec2.run_instances(
            ImageId=get_latest_ami(os),
            InstanceType=instance_type,
            KeyName=key_pair,
            SecurityGroupIds=[security_group],
    
            BlockDeviceMappings=[
                {
                    "DeviceName": "/dev/xvda",
                    "Ebs": {
                        "VolumeSize": disk_size,
                        "VolumeType": "gp3",
                        "DeleteOnTermination": True
                    }
                }
            ],
    
            TagSpecifications=[
                {
                    "ResourceType": "instance",
                    "Tags": [
                        {
                            "Key": "Name",
                            "Value": name
                        }
                    ]
                }
            ],
    
            MinCount=1,
            MaxCount=1
        )
        return json.dumps({
                "status": True,
                "message": "Creating an instance",
                "aws_response": response
            })
    except Exception as e:
        return json.dumps({
            "status": False,
            "message": "Error creating an instance",
            "error_type": type(e).__name__,
            "error": str(e)
        })

def get_latest_ami(os_name: str):
    """find ami image"""
    config = AMI_FILTERS[os_name]
    try:
        response = ec2.describe_images(
            Owners=[config["owner"]],
            Filters=[
                {
                    "Name": "name",
                    "Values": [config["name"]]
                },
                {
                    "Name": "architecture",
                    "Values": ["x86_64"]
                }
            ]
        )

        images = sorted(
            response["Images"],
            key=lambda x: x["CreationDate"],
            reverse=True
        )

        return images[0]["ImageId"]
    except Exception as e:
        return json.dumps({
            "status": False,
            "message": "Error finding AMI",
            "error_type": type(e).__name__,
            "error": str(e)
        })