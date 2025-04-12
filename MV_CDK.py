from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_iam as iam,  # Importar la librería de IAM
)
from constructs import Construct

class MiInstanciaEc2Stack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # VPC por defecto
        vpc = ec2.Vpc.from_lookup(self, "VPC", is_default=True)

        # Security Group
        sg = ec2.SecurityGroup(self, "MiSG",
            vpc=vpc,
            description="Permitir SSH y HTTP",
            allow_all_outbound=True
        )
        sg.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(22), "SSH")
        sg.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(80), "HTTP")

        # Buscar la AMI por nombre
        ami = ec2.MachineImage.lookup(
            name="Cloud9ubuntu22",
            owners=["self"],  # o el ID del owner de la AMI si es compartida
        )

        # ARN del rol de IAM 
        labrole_arn = "arn:aws:iam::174052614095:role/LabRole"

        # Crear una instancia EC2 con el rol asociado
        instancia = ec2.Instance(self, "MiEC2",
            instance_type=ec2.InstanceType("t3.micro"),
            machine_image=ami,
            vpc=vpc,
            key_name="vockey",
            security_group=sg,
            role=iam.Role.from_role_arn(self, "LabRole", labrole_arn),  # Asocia el rol
            block_devices=[ec2.BlockDevice(
                device_name="/dev/xvda",
                volume=ec2.BlockDeviceVolume.ebs(20)
            )]
        )
