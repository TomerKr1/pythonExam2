import json

def save_data(instance_id, instance_state, public_ip, lb_dns):
    
    verification_data = {
        "instance_id": instance_id,
        "instance_state": instance_state,
        "public_ip": public_ip,
        "load_balancer_dns": lb_dns
    }
    try:
        with open('aws_validation.json', 'w') as json_file:
            json.dump(verification_data, json_file, indent=3)
        print("Verification data saved successfully.")
    except Exception as e:
        print(f"Error saving verification): {e}")
