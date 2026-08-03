#list ec2 instances
from langchain.tools import tool

EC2_INSTANCES=[
    {
    "id": "i-02179214",
    "name": "web-server",
    "state": "stopped"
  },{
    "id": "i-02179255",
    "name": "app-server",
    "state": "stopped"
  },{
    "id": "i-02178123",
    "name": "db-server",
    "state": "terminated"
  }
]

@tool
def list_instances():
    """lists all the instances"""
    return EC2_INSTANCES

@tool
def get_instance_by_id(instance_id):
    """gets the instance by id"""
    for instance in EC2_INSTANCES:
        if instance["id"]==instance_id:
            return instance
    return "instance not found"

def get_instance_b_id(instance_id):
    """gets the instance by id"""
    for instance in EC2_INSTANCES:
        if instance["id"]==instance_id:
            return instance
    return "instance not found"

@tool
def restart_instance(instance_id: str):
    """restarts the instance by id"""
    instance = get_instance_b_id(instance_id)
    if isinstance(instance, str):
        return instance
    if instance["state"] == "terminated":
        return "the instance is terminated, cannot restart it"
    elif instance["state"] == "running":
        return "the instance is already running"
    elif instance["state"] == "stopped":
        instance["state"] = "running"
        return "the instance is restarting"
    else:
        return "instance not found"