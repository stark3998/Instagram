# -*- coding: utf-8 -*-
__author__ = ''

from instagram_scraper import app
from instagram_scraper.model.insta import User, Comment, Post
from instagram_scraper.schemas.insta import UserSchema
from flask import request, jsonify, render_template


@app.route('/api/v1/create_user', methods=['POST'])
def create_user():
    print(request.json)
    ob = User(**request.json)
    ob.save()
    result = UserSchema().dump(ob)
    return jsonify(result.data)

"""
@app.route('/api/v1/update_message/<message_id>', methods=['PATCH'])
def update_message(message_id):
    ob = Message.query.get(message_id)
    if ob:
        for key in request.json:
            setattr(ob, key, request.json[key])
        ob.update()
        result = MessageSchema().dump(ob)
        return jsonify(result.data)
    return jsonify({'error': "No Message found with id ({})".format(message_id)}), 500


@app.route('/api/v1/delete_message/<message_id>', methods=['DELETE'])
def delete_message(message_id):
    print(request.json)
    for m in MessageReceived.query.filter_by(message_id=message_id).all():
        m.delete()
    ob = Message.query.get(message_id)
    if ob:
        ob.delete()
        return jsonify({'id': ob.id})
    return jsonify({'error': "No Message found with id ({})".format(message_id)}), 500
"""

@app.route('/api/v1/users', methods=['GET'])
def messages():
    if request.method == 'GET':
        args = request.args.to_dict()
        args.pop('page', None)
        args.pop('per_page', None)
        per_page = int(request.args.get('per_page', 100))
        page = int(request.args.get('page', 1))
        data = User.query.filter_by(**args).order_by(User.created_at.desc()).offset((page - 1) * per_page).limit(
            per_page).all()
        data = UserSchema(many=True).dump(data).data
        response = jsonify({"result": data})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response


@app.route("/message")
def render_message():
    return render_template("message.html")

