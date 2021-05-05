from aws_cdk import (core,
                     aws_apigateway as apigateway,
                     aws_lambda as lambda_,
                     aws_iam as iam,
                     aws_dynamodb as dynamodb,
                     aws_apigatewayv2 as apigw,
                     aws_apigatewayv2_integrations as integrations)

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

        lambda_handler = lambda_.Function(self, "WordHandler",
                    runtime=lambda_.Runtime.NODEJS_10_X,
                    code=lambda_.Code.from_asset("resources/lambda"),
                    handler="words.main",
                    environment=dict(
                        DB_NAME=table.table_name
                        )
                    )

        table.grant_read_data(lambda_handler)

        # api_integration = integrations.LambdaWebSocketIntegration(handler=lambda_handler)
        api_integration = integrations.LambdaWebSocketIntegration(handler=lambda_handler)
        # Falla la integración, el LAMBDA_PROXY y el resultado
        #web_socket_api = apigw.WebSocketApi(self, 'words_api',
        #    default_route_options={"integration": api_integration}
        #)

        web_socket_route_options = apigw.WebSocketRouteOptions(integration=api_integration)
        web_socket_api = apigw.WebSocketApi(self, 'words_api', 
            default_route_options=web_socket_route_options
        )
        web_socket_api.add_route('na',
            integration=integrations.LambdaWebSocketIntegration(
                handler=lambda_handler
            )
        )
        """
        NO FUNCIONA
                web_socket_api.add_route("$default",
                    integration=api_integration
                )
        """
        # api_integration.bind(route=apigw.WebSocketRouteIntegrationBindOptions.., scope=self )

        api_stage = apigw.WebSocketStage(self, 'DevStage', 
            web_socket_api=web_socket_api,
            stage_name='dev',
            auto_deploy=True,
            )
        
        #web_socket_api.api_endpoint

        
        """
        api = apigateway.RestApi(self, "words-api",
                  rest_api_name="Words API",
                  description="This service serves words.")

        integration = apigateway.LambdaIntegration(handler,
                request_templates={"application/json": '{ "statusCode": "200" }'})

        api.root.add_method("GET", integration)
        """

        
