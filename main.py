from boto3Mission import  search_ALB, search_instance
from generate_tf import execute_terraform, generate_terraform
from get_user_input import user_choice, display_selections
from python_terraform import Terraform
from json_saving import save_data


main_menu = """What do you want to do?
1 - Choose AMI and Instance details
q - Exit
"""

selection = user_choice(main_menu, {"1": display_selections, "q": exit})
if selection is None:
    exit() 
terraform_geneate = generate_terraform(selection)  # generate the TF file


with open('generated_tf.tf', 'w') as f: # write the TF file
    f.write(terraform_geneate)
    print("successe creating of TF file")

#execute_terraform() # trying to run the TF, but i have some issues with the VPC.
# so i asked the GPT to generate me a 'fake EC2 instance, LB dns name for the next steps.
# it may be stock but you can '#' it so you can keep see the other functions.

print("-------------------------------")
fake_instance_id = "i-1234567890abcdef0"
fake_lb_dns_name = "fake-lb-dns-name.amazonaws.com"
fake_instance_state = "running"
fake_public_ip="3.92.102.45"

print(f"Fake Instance ID: {fake_instance_id}")
print(f"Fake LB DNS Name: {fake_lb_dns_name}")


# the part for Bot03 with mock 

print(f"Im now starting to search for your instance ID - { fake_instance_id}")
search_instance(fake_instance_id)

print("-----------------------------------------")
print(f"Im now starting to search for your Load balancer DNS Name - {fake_lb_dns_name} ")
search_ALB(fake_lb_dns_name)


print("-------------- JSON SAVING -----------------")
save_data(fake_instance_id, fake_instance_state, fake_public_ip, fake_lb_dns_name)
print("-------------- JSON SAVED -----------------")
