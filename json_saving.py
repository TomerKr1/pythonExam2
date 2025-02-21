import json

def save_data(instance_id, instance_state, public_ip, lb_dns):
    # saving as dict and then as json
    verification_data = {
        "instance_id": instance_id,
        "instance_state": instance_state,
        "public_ip": public_ip,
        "load_balancer_dns": lb_dns
    }
    try:
        with open('aws_validation.json', 'w') as json_file:
            json.dump(verification_data, json_file, indent=3) # the dump is use for change the dict to json
        print("Saving the data successfully")
    except Exception as e:
        print(f"Error saving verification): {e}")
