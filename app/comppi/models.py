from app.app_and_db import db


# Define the Protein data model.
class Protein(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    specieId = db.Column(db.Integer, nullable=False)
    proteinName = db.Column(db.String(255), nullable=False)
    proteinNamingConvention = db.Column(db.String(255), nullable=False)