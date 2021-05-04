#!/usr/bin/env python3
import os

from aws_cdk import core as cdk
from aws_cdk import core
from cdk_apigw_lambda_dynamodb.cdk_apigw_lambda_dynamodb_stack import CdkApigwLambdaDynamodbStack

app = core.App()
CdkApigwLambdaDynamodbStack(app, "CdkApigwLambdaDynamodbStack", )
app.synth()
