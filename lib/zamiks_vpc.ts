import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as elbv2 from 'aws-cdk-lib/aws-elasticloadbalancingv2';

export interface ZamiksVPCStackADVProps extends cdk.StackProps  {
    readonly vpcCidr: string;
}

export class ZamiksVPCStackADV extends cdk.Stack {
  public readonly sg_service:ec2.SecurityGroup;
  public readonly zamiks_vpc_adv:ec2.Vpc;
  public readonly lb:elbv2.ApplicationLoadBalancer;

  constructor(scope: Construct, id: string, props: ZamiksVPCStackADVProps) {
    super(scope, id,{...props,});


    this.zamiks_vpc_adv = new ec2.Vpc(this, 'zamiks_adv_vpc', {
      cidr: props?.vpcCidr,
      natGateways: 1,
      maxAzs: 3,
      subnetConfiguration: [
        {
          name: 'private-subnet-1',
          subnetType: ec2.SubnetType.PRIVATE_WITH_NAT,
          cidrMask: 24,
        },
        {
          name: 'public-subnet-1',
          subnetType: ec2.SubnetType.PUBLIC,
          cidrMask: 24,
        },
      ],
    });

    this.sg_service = new ec2.SecurityGroup(this, 'ZamiksSGService', { vpc: this.zamiks_vpc_adv });
    this.sg_service.addIngressRule(ec2.Peer.ipv4('0.0.0.0/0'), ec2.Port.tcp(80));
    this.sg_service.addIngressRule(ec2.Peer.ipv4('0.0.0.0/0'), ec2.Port.tcp(8081));

    this.lb = new elbv2.ApplicationLoadBalancer(this, 'ALB', {
      vpc:this.zamiks_vpc_adv,
      internetFacing: true
    });

  }
}
