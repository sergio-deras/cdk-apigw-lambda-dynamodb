from aws_cdk import core as cdk
from . import word_service

class CdkApigwLambdaDynamodbStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        word_service.WordService(self, "Word")