from aws_cdk import (core,
                     aws_apigateway as apigateway,
                     aws_lambda as lambda_,
                     aws_dynamodb as dynamodb)

from cloudcomponents.cdk_dynamodb_seeder import DynamoDBSeeder, Seeds
import os.path

class WordService(core.Construct):
    def __init__(self, scope: core.Construct, id: str):
        super().__init__(scope, id)

        table = dynamodb.Table(
            self,
            "Words",
            partition_key={'name': 'word', 'type': dynamodb.AttributeType.STRING},
            removal_policy=core.RemovalPolicy.DESTROY
        )

        dir_path = os.path.dirname(os.path.realpath(__file__))

        DynamoDBSeeder(self, "JsonFileSeeder",
                       table=table,
                       seeds=Seeds.from_json_file(os.path.join(dir_path, "../resources/db", "words.json"))
                       )

        handler = lambda_.Function(self, "WordHandler",
                    runtime=lambda_.Runtime.NODEJS_10_X,
                    code=lambda_.Code.from_asset("resources/lambda"),
                    handler="words.main",
                    environment=dict(
                        DB_NAME=table.table_name
                        )
                    )

        table.grant_read_data(handler)

        api = apigateway.RestApi(self, "words-api",
                  rest_api_name="Words API",
                  description="This service serves words.")

        integration = apigateway.LambdaIntegration(handler,
                request_templates={"application/json": '{ "statusCode": "200" }'})

        api.root.add_method("GET", integration)