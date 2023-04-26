from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods = ['GET', 'POST'])
def messages():
    if request.method == 'GET':
        created_at_messages = Message.query.order_by('created_at').all()
        sorted_messages = [message.to_dict() for message in created_at_messages]
        response = make_response(
            sorted_messages,
            200)

    elif request.method == 'POST':
        data = request.get_json()
        new_message = Message(
            body = data['body'],
            username = data['username']
        )

        db.session.add(new_message)
        db.session.commit()

        new_message_serial = new_message.to_dict()

        response = make_response(
            new_message_serial,
            200
        )

    return response

@app.route('/messages/<int:id>', methods = ['PATCH', 'DELETE'])
def messages_by_id(id):

    message = Message.query.filter_by(id = id).first()
    if request.method == 'PATCH':
        data = request.get_json()
        for key in data:
            setattr(message, key, data[key])

        db.session.add(message)
        db.session.commit()

        message_serial = message.to_dict()

        response = make_response(
            message_serial,
            200
        )
    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()

        response = make_response(
            {'message': 'Message has been deleted'}, 
            200
        )

    return response

if __name__ == '__main__':
    app.run(port=5555)
