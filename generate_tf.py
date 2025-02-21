from jinja2 import Template
from python_terraform import Terraform

"""
in this file we are generating the TF file with the template with the users selection by the menu.
also we are running the tf with the commands and printing also the output.
we can also see the file that we are generating with the selection by the name "generated_tf.tf"

I had a prolbem with the VPC but the file builded in the currect way and i also added a depends on,
for example in the listener and the target group.
"""



def generate_terraform(selection):
    terraform_template = """
    
provider "aws" { 
  region = "{{ region }}" 
}
    
    
resource "aws_instance" "web_server" {
  ami               = "{{ ami }}"
  instance_type     = "{{ instance_type }}"
  availability_zone = "{{ availability_zone }}"
  tags = {
    Name = "WebServer"
  }
}

resource "aws_lb" "application_lb" {
  name               = "{{ load_balancer_name }}"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.lb_sg.id]
  subnets            = aws_subnet.public[*].id
 depends_on         = [aws_security_group.lb_sg]
}

resource "aws_security_group" "lb_sg" {
  name        = "TomerK-lb_security_group"
  description = "Allow HTTP inbound traffic"

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_lb_listener" "http_listener" {
  load_balancer_arn = aws_lb.application_lb.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.web_target_group.arn
  }
  depends_on = [aws_lb_target_group.web_target_group] # added!
}

resource "aws_lb_target_group" "web_target_group" {
  name     = "tomer-web-target-group"
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_vpc.main.id
}

resource "aws_lb_target_group_attachment" "web_instance_attachment" {
  target_group_arn = aws_lb_target_group.web_target_group.arn
  target_id        = aws_instance.web_server.id
}

resource "aws_subnet" "public" {
  count = 2
  vpc_id = aws_vpc.main.id
  cidr_block = "10.0.${count.index}.0/24"
  availability_zone = element(["us-east-1a", "us-east-1b"], count.index)
}
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
  }
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id
}
 resource "aws_route" "public_route" {
    route_table_id         = aws_route_table.public.id
    destination_cidr_block = "0.0.0.0/0"
    gateway_id             = aws_internet_gateway.main.id
  }
  resource "aws_route_table_association" "public_association" {
    count          = 2
    subnet_id      = aws_subnet.public[count.index].id
    route_table_id = aws_route_table.public.id
  }
 resource "aws_vpc" "main" {
    cidr_block = "10.0.0.0/16"
  }
    """

    
    template = Template(terraform_template) # template with jinja2

    # here we are putting the values
    rendered_template = template.render( 
        ami=selection['ami'],
        instance_type=selection['instance_type'],
        region=selection['region'],
        availability_zone=selection['availability_zone'],
        load_balancer_name=selection['load_balancer_name']
    )

    return rendered_template


def execute_terraform():
    tf = Terraform()
    """
      the 'capture_output=True' is for catching the output of the command
      the 'var_file' is for the file wee are usin for plan and init

    """
    # Init
    print("Running terraform init")
    init_output = tf.init(capture_output=True) 

    #Plan
    print("Running terraform plan...")
    planin_output = tf.plan(capture_output=True)
    if "Error" in planin_output[2]:
        print(f"Error during terraform plan: {planin_output[2]}")
    else:
        print(planin_output[1]) # printing the output of the planing 

    # Apply terraform
    print("Running terraform apply...")
    applying_output = tf.apply(capture_output=True)
    if "Error" in applying_output[2]:  
        print(f"Error during terraform apply: {applying_output[2]}")
    else:
        print(applying_output[1])  # printing the output of the apply
