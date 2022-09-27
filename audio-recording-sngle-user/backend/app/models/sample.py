from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from db.database import Base


class Sample(Base):
    __tablename__ = "sample"
    id = Column(Integer, primary_key=True, autoincrement=True)
    transcription = Column(String(100000), nullable=False)
    filename = Column(String(100000), nullable=True, unique=True)

    def __repr__(self):
        return f"<id: {self.id}, recorded: {'True' if self.filename else 'False'}>"

    @staticmethod
    def get_all_samples(db):
        return db.query(Sample).all()

    @staticmethod
    def get_sample_by_id(db, _id):
        return db.query(Sample).filter(Sample.id == _id).first()

    @staticmethod
    def get_unrecorded_samples(db,  n):
        return db.query(Sample).filter(Sample.filename.is_(None)).limit(n).all()

    def to_dict(self):
        return {"id": self.id, "transcription": self.transcription, 'filename': self.filename}
