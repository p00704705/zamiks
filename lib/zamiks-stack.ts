import { Stack, StackProps } from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { App, Duration } from "aws-cdk-lib";
import {ZamiksECRStack} from './zamiks_ecr';
import {ZamiksVPCStackADV} from './zamiks_vpc';
import * as cdk from 'aws-cdk-lib';

export class ZamiksStack extends Stack {
  constructor(scope: App, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const ZamiksVPCStackADVProps = {
      vpcCidr:"192.168.0.0/16"
    };

    const ADVZamiksVPCStack = new ZamiksVPCStackADV(this,"zamiks_vpc_adv",ZamiksVPCStackADVProps)

    const ZamiksECRStackProps = {
      adv_vpc:ADVZamiksVPCStack.zamiks_vpc_adv,
      sec_group:ADVZamiksVPCStack.sg_service,
      lb:ADVZamiksVPCStack.lb
    };

    const ZamiksECRServer = new ZamiksECRStack(this, "zamiks_ecr_repo",ZamiksECRStackProps);
    
  }
}
