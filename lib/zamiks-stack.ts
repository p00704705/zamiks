import { Stack, StackProps } from 'aws-cdk-lib';
import { Construct } from 'constructs';
// import * as sqs from 'aws-cdk-lib/aws-sqs';
import {ZamiksECRStack} from './zamiks_ecr'
export class ZamiksStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);


    const ZamiksECRStack_Server = new ZamiksECRStack(this, "zamiks_ecr_repo");
    
 
  }
}
