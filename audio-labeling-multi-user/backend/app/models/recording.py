from sqlalchemy import Column, Integer, Boolean

from db.database import Base


class Recording(Base):
    __tablename__ = "recording"
    id = Column(Integer, primary_key=True, autoincrement=True)
    sample_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    is_recorded = Column(Boolean)

    def __repr__(self):
        return f"<id: {self.id}, user_id: {self.user_id}, sample_id: {self.sample_id}, Recordings: {self.recordings}>"

    @staticmethod
    def get_all_recordings(db):
        return db.query(Recording).all()

    @staticmethod
    def get_recording_by_user_id_and_sample_id(db, sample_id, user):
        return db.query(Recording).filter(
            Recording.sample_id == sample_id,
            Recording.user_id == user.id
        ).first()

    def to_dict(self):
        return {"id": self.id, "sample_id": self.sample_id, 'user_id': self.user_id, 'recordings': self.recordings}
