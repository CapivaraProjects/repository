from repository.base import Base
from database.Plant import Plant
from database.Disease import Disease
from database.Type import Type
from database.Image import Image
from database.Analysis import Analysis
from database.AnalysisResult import AnalysisResult
from database.Classifier import Classifier


def test_connection():
    base = Base('capivara',
                'test',
                '127.0.0.1',
                '5432',
                'green_eyes')
    session = base.session_factory()
    image_query = session.query(Image)
    session.close()
    assert type(image_query.all()) == list
