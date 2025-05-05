from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import db, User, Message

messages_bp = Blueprint('messages_bp', __name__, url_prefix='/api/messages')

@messages_bp.route('/<int:other_id>', methods=['GET'])
@jwt_required()
def get_conversation(other_id):
    me = User.query.filter_by(username=get_jwt_identity()).first_or_404()
    # fetch messages where I am sender or recipient with other_id
    convo = Message.query.filter(
        ((Message.sender_id == me.id) & (Message.recipient_id == other_id)) |
        ((Message.sender_id == other_id) & (Message.recipient_id == me.id))
    ).order_by(Message.timestamp).all()

    return jsonify([
        {
            'id': msg.id,
            'from_me': msg.sender_id == me.id,
            'content': msg.content,
            'timestamp': msg.timestamp.isoformat()
        }
        for msg in convo
    ]), 200

@messages_bp.route('', methods=['POST'])
@jwt_required()
def send_message():
    data = request.get_json() or {}
    recipient_id = data.get('recipient_id')
    content      = data.get('content','').strip()
    if not recipient_id or not content:
        return jsonify(msg="recipient_id and content required"), 400

    me = User.query.filter_by(username=get_jwt_identity()).first_or_404()
    # ensure recipient exists
    User.query.get_or_404(recipient_id)

    msg = Message(sender_id=me.id, recipient_id=recipient_id, content=content)
    db.session.add(msg)
    db.session.commit()
    return jsonify(msg="Message sent", message_id=msg.id), 201
