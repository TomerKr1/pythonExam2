from typing import Callable

selection = {}

def user_choice(menu: str, actions: dict[str, Callable]):
   
    user_input  = input(menu).strip()
    if user_input == "q":
        return None  
    try:
        return actions[user_input]()
    except KeyError:
        print("Unknown action, try again")
        return None

def choose_ami():
    print("Choose an AMI:")
    print("1. Ubuntu (ami-???), 2. Amazon Linux (ami-???)")
    ami_choice = input("Enter your choice (1 or 2): ")
    if ami_choice == "1":
        ami = "ami-0b0ea68c435eb488d"
    elif ami_choice == "2":
        ami = "ami-0ff8a91507f77f867"
    else:
        print("Invalid choice, defaulting to Ubuntu")
        ami = "ami-ubuntu-?????"
    return ami

def choose_instance_type():
    print("Choose an Instance Type:")
    print("1. t3.small, 2. t3.medium")
    instance_type_choice = input("Enter your choice (1 or 2): ")
    if instance_type_choice == "1":
        instance_type = "t3.small"
    elif instance_type_choice == "2":
        instance_type = "t3.medium"
    else:
        print("Invalid choice, defaulting to t3.small")
        instance_type = "t3.small"
    return instance_type

def choose_region():
    print("Choose a region:")
    print("Available region: us-east-1")
    region_choice = input("Enter your region (default is us-east-1): ")
    if region_choice.lower() != "us-east-1":
        print("Invalid region, defaulting to us-east-1")
        region = "us-east-1"
    else:
        region = region_choice
    return region

def choose_availability_zone():
    print("Choose an Availability Zone:")
    print("Available zones: us-east-1a, us-east-1b")
    az_choice = input("Enter your Availability Zone (us-east-1a or us-east-1b): ")
    if az_choice not in ["us-east-1a", "us-east-1b"]:
        print("Invalid choice, defaulting to us-east-1a")
        availability_zone = "us-east-1a"
    else:
        availability_zone = az_choice
    return availability_zone

def choose_load_balancer_name():
    load_balancer_name = input("Enter a custom name for the Load Balancer: ")
    return load_balancer_name

def get_user_input():
    ami = choose_ami()
    instance_type = choose_instance_type()
    region = choose_region()
    availability_zone = choose_availability_zone()
    load_balancer_name = choose_load_balancer_name()

    selections = {
        "ami": ami,
        "instance_type": instance_type,
        "region": region,
        "availability_zone": availability_zone,
        "load_balancer_name": load_balancer_name
    }

    return selections

def display_selections():
    selections = get_user_input()  # Get the user input
    return selections  # Return the selections instead of printing them
