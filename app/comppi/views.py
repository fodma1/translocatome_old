from app.app_and_db import db

from models import Protein
from flask import jsonify


def query_database(query_string):
    # query_result = [(row.id, row.specieId, row.proteinName, row.proteinNamingConvention) for row in db.session.query(Protein).filter(Protein.proteinName.startswith(query_string))]
    # query_result = jsonify(json_list=db.session.query(
    #     Protein).filter(
    #     Protein.proteinName.startswith(query_string)).all())
    query_result = jsonify(json_list=[(row.id,
                            row.specieId,
                            row.proteinName,
                            row.proteinNamingConvention) for row in db.session.query(
        Protein).filter(
        Protein.proteinName.startswith(query_string)).all()])
    return query_result