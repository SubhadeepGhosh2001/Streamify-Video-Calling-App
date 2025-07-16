from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import enum

db = SQLAlchemy()

# Optional: Enum for status
class FriendRequestStatus(enum.Enum):
    pending = "pending"
    accepted = "accepted"

class FriendRequest(db.Model):
    __tablename__ = "friend_requests"

    id = db.Column(db.Integer, primary_key=True)

    sender_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    status = db.Column(
        db.Enum(FriendRequestStatus),
        default=FriendRequestStatus.pending,
        nullable=False
    )

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Optional relationships (for JOINs and easy access)
    sender = db.relationship("User", foreign_keys=[sender_id], backref="sent_requests")
    recipient = db.relationship("User", foreign_keys=[recipient_id], backref="received_requests")
