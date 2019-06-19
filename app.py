import os
import boto3
import json
from flask import Flask, jsonify, request

app = Flask(__name__)

USERS_TABLE = os.environ['USERS_TABLE']
IS_OFFLINE = os.environ.get('IS_OFFLINE')

if IS_OFFLINE:

    client = boto3.client(
        'dynamodb',
        region_name='localhost',
        endpoint_url='http://localhost:8000'
    )

else:
    client = boto3.client('dynamodb',region_name='sa-east-1')


@app.route("/")
def hello():
    return "Hello, sucessful test with a web application using flask and serverless!!"


@app.route("/user/get/<string:user_id>", methods=["GET"])
def get_user(user_id):
    resp = client.get_item(
        TableName=USERS_TABLE,
        Key={
            'userId': { 'S': user_id }
        }
    )
    item = resp.get('Item')
    if not item:
        return jsonify({'error': 'User does not exist'}), 404
    return jsonify({
        'userId': item.get('userId').get('S'),
        'name': item.get('name').get('S')
    })



@app.route("/users/getAll", methods=["GET"])
def get_all_user():
    response = client.scan(
        TableName=USERS_TABLE,
    )
    itens = response.get('Items')
    return jsonify(itens)
    


@app.route("/user/create", methods=["POST"])
def create_user():
    user_id = request.json.get('userId')
    name = request.json.get('name')
    if not user_id or not name:
        return jsonify({'error': 'Please provide userId and name'}), 400

    resp = client.put_item(
        TableName=USERS_TABLE,
        Item={
            'userId': {'S': user_id },
            'name': {'S': name }
        }
    )
    return jsonify({
        'userId': user_id,
        'name': name
    })

@app.route("/user/edit/<string:user_id>", methods=["PUT"])
def edit_user():
    user_id = request.json.get('userId')
    name = request.json.get('name')
    if not user_id or not name:
        return jsonify({'error': 'Please provide userId and name'}), 400

    resp = client.put_item(
        TableName=USERS_TABLE,
        Item={
            'userId': {'S': user_id },
            'name': {'S': name }
        },
        ExpressionAttributeValues={'userId': {'S': user_id }}
    )
    return jsonify({
        'userId': user_id,
        'name': name
    })



@app.route("/user/remove/<string:user_id>", methods=["DELETE"])
def delete_user(user_id):
    client.delete_item(
        TableName=USERS_TABLE,
        Key={
            'userId': {'S': user_id }
        }
    )
    return jsonify({'message':'User with id '+user_id+' was deleted!'}),200