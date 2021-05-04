
const AWS = require('aws-sdk');
const DB = process.env.DB_NAME;
var docClient = new AWS.DynamoDB.DocumentClient();

exports.main = async function(event, context) {
  try {
    var method = event.httpMethod;

    if (method === "GET") {
      if (event.path === "/") {
        var params = {
          TableName: DB,
          Key: {
            'word': {S: 'hi'}
          }
        };

        docClient.get(params).promise()
        .then(result => {
          const response = {
            statusCode: 200,
            body:  JSON.stringify(result.Item),
          };
          callback(null, response);
        })
        .catch(error => {
          console.error(error);
          callback(new Error('Couldn\'t fetch candidate.'));
          return;
        });
      }
    } else {
      //Only Get
      return {
        statusCode: 400,
        headers: {},
        body: "We only accept GET /"
      };
    }    
  } catch(error) {
    var body = error.stack || JSON.stringify(error, null, 2);
    return {
      statusCode: 400,
        headers: {},
        body: JSON.stringify(body)
    }
  }
}
