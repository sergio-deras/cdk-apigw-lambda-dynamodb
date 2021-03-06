const AWS = require('aws-sdk');
const DB = process.env.DB_NAME;
var docClient = new AWS.DynamoDB.DocumentClient();

const params = {
  TableName : process.env.DB_NAME,
  Key: {
    "word": 'Hi'
  }
}

async function getItem(){
  try {
    const data = await docClient.get(params).promise();
    return data.Item;
  } catch (err) {
    return err
  }
}

exports.main = async (event, context) => {
  try {
    const data = await getItem()
    return {
      statusCode: 200,
      headers: {},
      body: JSON.stringify(data)
    }
  } catch (err) {
    return { error: err }
  }
}

