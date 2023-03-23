import logging
from flask import request, abort
from flask_cors import CORS

from nauron import Nauron

import settings

logger = logging.getLogger("gunicorn.error")

# Define application
app = Nauron(__name__, timeout=settings.MESSAGE_TIMEOUT, mq_parameters=settings.MQ_PARAMS)
CORS(app)

neural_morph = app.add_service(name=settings.SERVICE_NAME, remote=settings.DISTRIBUTED)

if not settings.DISTRIBUTED:
    from neural_morph_tagger_worker import NeuralMorphTaggerWorker

    neural_morph.add_worker(NeuralMorphTaggerWorker())

#
# Endpoints for NeuralMorphTaggerWorker
#

@app.post('/estnltk/tagger/neural_morph_disamb')
def tagger_neural_morph_disamb():
    if request.content_length > settings.MAX_CONTENT_LENGTH:
        abort(413)
    response = neural_morph.process_request(content=request.json)
    return response

@app.get('/estnltk/tagger/neural_morph_disamb/about')
def tagger_neural_morph_disamb_about():
    return 'Tags neural morph disambiguation using EstNLTK NeuralMorphTagger\'s webservice. '+\
           'Uses softmax emb_cat_sum model.'


@app.get('/estnltk/tagger/neural_morph_disamb/status')
def tagger_neural_morph_disamb_status():
    return 'OK'


if __name__ == '__main__':
    app.run()
