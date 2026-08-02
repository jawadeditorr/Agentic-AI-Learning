#list ec2 instances
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
class ec2:
    EC2_INSTANCES=[]
    def __init__(self):
        self.EC2_INSTANCES=[
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

    def list_instances(self):
        return self.EC2_INSTANCES
    
    def get_instance_by_id(self,instance_id):
        for instance in self.EC2_INSTANCES:
            if instance["id"]==instance_id:
                return instance
        return None
            
    def restart_instance(self, instance_id):
        instance = self.get_instance_by_id(instance_id)
        # pyrefly: ignore [unsupported-operation]
        if instance["state"] == "terminated":
            return "the instance is terminated, cannot restart it"
        elif instance["state"] == "running":
            return "the instance is already running"
        elif instance["state"] == "stopped":
            instance["state"] == "running"
            return "the instance is restarting"
        else:
            return "instance not found"

ec2_obj = ec2()

print(ec2_obj.restart_instance("i-02178123"))
print(ec2_obj.get_instance_by_id("i-02178123"))