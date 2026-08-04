#list ec2 instances
from langchain.tools import tool
import sys
import boto3

ec2 = boto3.client('ec2')

@tool
def list_instances():
    """lists all the instances"""
    response = ec2.describe_instances()
    for Reservations in response:
        for Instances in Reservations['Instances']:
            return Instances['InstanceId'],Instances['Tags']

@tool
def get_instance_by_id(instance_id):
    """gets the instance by id"""
    response = ec2.describe_instances()
    for Reservations in response:
        for Instances in Reservations['Instances']:
            if instance_id==Instances['InstanceId']:
                return Instances['InstanceId']
    return "instance not found"

def get_instance_b_id(instance_id):
    """gets the instance by id as a helper function for a tool"""
    response = ec2.describe_instances()
    for Reservations in response:
        for Instances in Reservations['Instances']:
            if instance_id==Instances['InstanceId']:
                return Instances['InstanceId'],Instances['State']
    return "instance not found","not found"

@tool
def restart_instance(instance_id,state):
    """restarts the instance by id"""
    instance_id,state = get_instance_b_id(instance_id)

    #instance not found
    if instance_id == "instance not found" and state == "notfound":
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
        response = ec2.start_instances(
            InstanceIds=[
                instance_id,
            ],
        )
        return "the instance is restarting",response
    else:
        return "instance not found"