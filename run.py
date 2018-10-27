from app import app, db
from app.models import Artist,Query, Song

@app.shell_context_processor
def make_shell_context():
    return{
        'db': db,
        'Artist': Artist,
        'Query':Query,
        'Song':Song
    }
