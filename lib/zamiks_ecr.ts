import { App, Duration } from "aws-cdk-lib";
import * as cdk from 'aws-cdk-lib';
import { Stack, StackProps } from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as ecs from 'aws-cdk-lib/aws-ecs';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as ecr from 'aws-cdk-lib/aws-ecr';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as ecs_patterns from 'aws-cdk-lib/aws-ecs-patterns';
import * as elbv2 from 'aws-cdk-lib/aws-elasticloadbalancingv2';
import { DockerImageAsset } from 'aws-cdk-lib/aws-ecr-assets';
import * as path from 'path';
import * as ecrdeploy from 'cdk-ecr-deployment';

export class ZamiksECRStack extends cdk.Stack {
    constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);


    const image = new DockerImageAsset(this, 'CDKDockerImage', {
      directory: path.join(__dirname, 'dockerfiles'),
      });

    const zamiks_repository = new ecr.Repository(this, "ZamiksECR", {
      repositoryName: "zamiks_ecr_repo"
    });
    new ecrdeploy.ECRDeployment(this, 'DeployDockerImage', {
      src: new ecrdeploy.DockerImageName(image.imageUri),
      dest: new ecrdeploy.DockerImageName("079409546332.dkr.ecr.us-east-1.amazonaws.com/zamiks_ecr_repo"),
    });

    const zamiks_vpc = new ec2.Vpc(this, "zamiks-vpc", {
      cidr: "10.1.0.0/16",
      natGateways: 1,
      subnetConfiguration: [
        {  cidrMask: 24, subnetType: ec2.SubnetType.PUBLIC, name: "Public" },
        {  cidrMask: 24, subnetType: ec2.SubnetType.PRIVATE_ISOLATED, name: "Private" }
        ],
      maxAzs: 3 // Default is all AZs in region
    });

    const zamiks_cluster = new ecs.Cluster(this, "ZamiksCluster", {
      vpc: zamiks_vpc
    });

    const zamiks_executionRolePolicy =  new iam.PolicyStatement({
      effect: iam.Effect.ALLOW,
      resources: ['*'],
      actions: [
                "ecr:GetAuthorizationToken",
                "ecr:BatchCheckLayerAvailability",
                "ecr:GetDownloadUrlForLayer",
                "ecr:BatchGetImage",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ]
    });
    
    const fargateTaskDefinition = new ecs.FargateTaskDefinition(this, 'ApiTaskDefinition', {
      memoryLimitMiB: 2048,
      cpu: 1024,
    });

    fargateTaskDefinition.addToExecutionRolePolicy(zamiks_executionRolePolicy);
    fargateTaskDefinition.addToTaskRolePolicy(new iam.PolicyStatement({
      effect: iam.Effect.ALLOW,
      resources: ['*'],
      actions: ['dynamodb:*']
    }));
    
    const container = fargateTaskDefinition.addContainer("backend", {
      // Use an image from Amazon ECR
      image: ecs.ContainerImage.fromRegistry(zamiks_repository.repositoryUri),
      logging: ecs.LogDrivers.awsLogs({streamPrefix: 'zamiks'}),
      environment: { 

      }
      // ... other options here ...
    });
    
    container.addPortMappings({
      containerPort: 8081
    });

    const sg_service = new ec2.SecurityGroup(this, 'MySGService', { vpc: zamiks_vpc });
    sg_service.addIngressRule(ec2.Peer.ipv4('0.0.0.0/0'), ec2.Port.tcp(80));
    sg_service.addIngressRule(ec2.Peer.ipv4('0.0.0.0/0'), ec2.Port.tcp(8081));

    const service = new ecs.FargateService(this, 'Service', {
      cluster: zamiks_cluster,
      taskDefinition: fargateTaskDefinition,
      desiredCount: 2,
      assignPublicIp: false,
      securityGroups: [sg_service]
    });
    
    // Setup AutoScaling policy
    const scaling = service.autoScaleTaskCount({ maxCapacity: 6, minCapacity: 2 });
    scaling.scaleOnCpuUtilization('CpuScaling', {
      targetUtilizationPercent: 50,
      scaleInCooldown: Duration.seconds(60),
      scaleOutCooldown: Duration.seconds(60)
    });

    const lb = new elbv2.ApplicationLoadBalancer(this, 'ALB', {
      vpc:zamiks_vpc,
      internetFacing: true
    });

    const listener = lb.addListener('Listener', {
      port: 8081,
      protocol: elbv2.ApplicationProtocol.HTTP
      
    });

    listener.addTargets('Target', {
      port: 8081,
      protocol: elbv2.ApplicationProtocol.HTTP,
      targets: [service],
      healthCheck: { path: '/api/' }
    });

    listener.connections.allowDefaultPortFromAnyIpv4('Open to the world');
    }
}