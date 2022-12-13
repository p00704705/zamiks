import * as codecommit from 'aws-cdk-lib/aws-codecommit';
import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as codebuild from 'aws-cdk-lib/aws-codebuild';
import * as codepipeline from 'aws-cdk-lib/aws-codepipeline';
import * as codepipeline_actions from 'aws-cdk-lib/aws-codepipeline-actions';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as ecs from 'aws-cdk-lib/aws-ecs';

export interface ZamiksCCCPStackProps extends cdk.StackProps  {
    readonly service: ecs.FargateService;
}

export class ZamiksCCCPStack extends cdk.Stack {

  constructor(scope: Construct, id: string, props: ZamiksCCCPStackProps) {
    super(scope, id,{...props,});


    const code = new codecommit.Repository(this, 'ZamiksRepository' ,{
      repositoryName: 'zamiks_codecommit_repo',
      description: 'flask based source backend.', // optional property
    });

    const project = new codebuild.PipelineProject(this, 'MyProject',{
      environment: {
        buildImage: codebuild.LinuxBuildImage.STANDARD_2_0,
        privileged: true
      },
    });
    const buildRolePolicy =  new iam.PolicyStatement({
      effect: iam.Effect.ALLOW,
      resources: ['*'],
      actions: [
                "ecr:GetAuthorizationToken",
                "ecr:BatchCheckLayerAvailability",
                "ecr:GetDownloadUrlForLayer",
                "ecr:GetRepositoryPolicy",
                "ecr:DescribeRepositories",
                "ecr:ListImages",
                "ecr:DescribeImages",
                "ecr:BatchGetImage",
                "ecr:InitiateLayerUpload",
                "ecr:UploadLayerPart",
                "ecr:CompleteLayerUpload",
                "ecr:PutImage"
            ]
    });
    project.addToRolePolicy(buildRolePolicy);
    
    const sourceOutput = new codepipeline.Artifact();
    const buildOutput = new codepipeline.Artifact();
    const sourceAction = new codepipeline_actions.CodeCommitSourceAction({
      actionName: 'CodeCommit',
      repository: code,
      output: sourceOutput,
    });
    const buildAction = new codepipeline_actions.CodeBuildAction({
      actionName: 'CodeBuild',
      project,
      input: sourceOutput,
      outputs: [buildOutput],
    });
    
    new codepipeline.Pipeline(this, 'ZamiksPipeline', {
      stages: [
        {
          stageName: 'Source',
          actions: [sourceAction],
        },
        {
          stageName: 'Build',
          actions: [buildAction],
        },
        {
          stageName: 'Deploy',
          actions: [
            new codepipeline_actions.EcsDeployAction({
              actionName: "ECS-Service",
              service: props.service, 
              input: buildOutput
            }
            )
          ]
        }
      ],
    });

}}