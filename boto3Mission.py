import boto3


"""
in this file we are using the boto3 for getting the EC2 and the ALB.
I had a problem with creating it, so i asked the GPT to generate me a fake EC2 instance and ALB.
first we are retrive all the intsnce and the ALB too, and then searchin for the fake ID and DNS name.
ofc we are not going to find it, so we are asking the user if he wants to see all the instnces and albs
"""


def get_instances():
    ec2_client = boto3.client("ec2")
    try:
        response = ec2_client.describe_instances() # return a dictionary with all the instances
        instances = response["Reservations"] #
        all_instances = []
        for reservation in instances:
            for instance in reservation["Instances"]:
                instance_id = instance.get("InstanceId", "No ID") # the no id is the default value if the key is not found
                instance_type = instance.get("InstanceType", "No instance type")
                instance_state = instance["State"]["Name"]
                all_instances.append({
                    "InstanceId": instance_id,
                    "InstanceType": instance_type,
                    "InstanceState": instance_state
                })
        
        return all_instances
    except Exception as e:
        print(f"Error fetching EC2 instances: {e}")
        return []

def printing_all_instances(instances):
    for instance in instances:
        print(f"Instance ID: {instance['InstanceId']}")
        print(f"Instance Type: {instance['InstanceType']}")
        print(f"Instance State: {instance['InstanceState']}")
        print("-----------------------------------------")


def search_instance(instanceid: str):
   
    all_instances = get_instances()
    instnace_found = [instance for instance in all_instances if instance["InstanceId"] == instanceid] 
    # much more easier and readable to search
    
    if instnace_found:
        print(f"Found Instance ID: {instnace_found['InstanceId']}")
        print(f"Instance Type: {instnace_found['InstanceType']}")
    else:
        print(f"Instance with ID {instanceid} not found.")
        choice = input("Do you want to see all the other instances? (yes/no): ").lower()
        
        if choice.lower() == 'yes':
            print("Listing all EC2 instances:")
            printing_all_instances(all_instances)
           
        else:
            print("Exiting without listing all instances.")

def get_all_alb():
    elbv2_client = boto3.client("elbv2")
    try:
     
        response = elbv2_client.describe_load_balancers()
        all_albs = []
        
        for alb in response["LoadBalancers"]:
            alb_name = alb.get("LoadBalancerName", "No Name")
            alb_state = alb["State"]["Code"]
            alb_dns_name = alb.get("DNSName", "No DNS Name")
            
            all_albs.append({
                "LoadBalancerName": alb_name,
                "State": alb_state,
                "DNSName": alb_dns_name
            })
        
        return all_albs
    except Exception as e:
        print(f"Error fetching ALB details: {e}")
        return []    
 
def print_alb(all_albs):
    for alb in all_albs:
        print(f"ALB Name: {alb['LoadBalancerName']}")
        print(f"State: {alb['State']}")
        print(f"DNS Name: {alb['DNSName']}")
        print("-----------------------------------------")
 
    
def search_ALB(albDNS: str):
   
    all_albs = get_all_alb()
    alb_found = [albdns for albdns in all_albs if albdns["DNSName"] == albDNS] 
    # much more easier and readable to search
    
    if alb_found:
        print(f"Found ALB with DNS Name: {alb_found['DNSName']}")
        print(f"ALB Name: {alb_found['LoadBalancerName']}")
        print(f"State: {alb_found['State']}")
    else:
        print(f"ALB with DNS Name {albDNS} not found.")
        choice = input("Do you want to see all the other ALBs? (yes/no): ").lower()
        if choice.lower() == 'yes':
            print("Listing all ALBs:")
            print_alb(all_albs)
        else:
            print("Bye")
            
            
