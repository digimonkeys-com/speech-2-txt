from sqlalchemy import Column, Integer, String

from db.database import Base


class Sample(Base):
    __tablename__ = "sample"
    id = Column(Integer, primary_key=True, autoincrement=True)
    transcription = Column(String(100000), nullable=False)

    def __repr__(self):
        return f"<id: {self.id}, transcription: {self.transcription}>"

    @staticmethod
    def get_all_samples(db):
        return db.query(Sample).all()

    @staticmethod
    def get_sample_by_id(db, _id):
        return db.query(Sample).filter(Sample.id == _id).first()

    def to_dict(self):
        return {"id": self.id, "transcription": self.transcription}
