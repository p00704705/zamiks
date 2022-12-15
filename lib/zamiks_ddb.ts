import { Stack, StackProps } from 'aws-cdk-lib';
import * as appScaling from 'aws-cdk-lib/aws-applicationautoscaling';
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';
import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';

export interface ZamiksDynamodbStackProps extends cdk.StackProps  {
    readonly tableName: string;
    readonly partitionKeyName: string;

}

export class ZamiksDynamodbStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: ZamiksDynamodbStackProps) {
    super(scope, id, props);

    const dynamoDBTable = new dynamodb.Table(this, props.tableName, {
      partitionKey: {
        name: props.partitionKeyName,
        type: dynamodb.AttributeType.STRING
      },
    });
    
    const readScaling = dynamoDBTable.autoScaleReadCapacity({ minCapacity: 1, maxCapacity: 10 })
    readScaling.scaleOnUtilization({
      targetUtilizationPercent: 65
    })
    const writeScaling = dynamoDBTable.autoScaleWriteCapacity({ minCapacity: 1, maxCapacity: 10 })
    writeScaling.scaleOnUtilization({
      targetUtilizationPercent: 65
    })
    writeScaling.scaleOnSchedule('ScaleUpInMorning', {
      schedule: appScaling.Schedule.cron({hour: '6', minute: '30'}),
      maxCapacity: 10,
      minCapacity: 5,
    })
    writeScaling.scaleOnSchedule('ScaleDownInNight', {
      schedule: appScaling.Schedule.cron( { hour: '22', minute: '00' }),
      maxCapacity: 5,
      minCapacity: 1,
    })
  }
}