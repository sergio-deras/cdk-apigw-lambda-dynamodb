## Pre-reqs
* npm (latest)
* python (3.x)
* aws cli (latest)
* aws cdk (latest)
* aws cli must have a profile configured with access to create the required infrastructure

## How to deploy
<code>
git clone https://github.com/sergio-deras/cdk-apigw-lambda-dynamodb
cd cdk-apigw-lambda-dynamodb
cdk bootstrap "aws://<account>/<region>"
cdk synth
cdk deploy
<code>
