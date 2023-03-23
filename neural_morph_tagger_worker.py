import logging
from typing import Dict

from nauron import Response, Worker
from marshmallow import Schema, fields, ValidationError

from estnltk import Text
from estnltk.converters import layer_to_dict
from estnltk.converters import json_to_layers

from neural_morph_tagger import SoftmaxEmbCatSumTagger

import settings

logger = logging.getLogger(settings.SERVICE_NAME)


class NeuralMorphTaggerRequestSchema(Schema):
    text = fields.Str(required=True)
    meta = fields.Raw(required=True)
    layers = fields.Str(required=True)
    output_layer = fields.Str(required=False)
    parameters = fields.Raw(required=False, allow_none=True)


class NeuralMorphTaggerWorker(Worker):
    def __init__(self, model_dir: str = "softmax_emb_cat_sum/"):
        self.schema = NeuralMorphTaggerRequestSchema
        self.tagger = SoftmaxEmbCatSumTagger( output_layer='neural_morph_analysis', \
                                              model_dir=model_dir )

    def process_request(self, content: Dict, _: str) -> Response:
        try:
            logger.debug(content)
            content = self.schema().load(content)
            text = Text(content["text"])
            text.meta = content["meta"]
            layers = json_to_layers(text, json_str=content['layers'])
            for layer in Text.topological_sort(layers):
                text.add_layer(layer)
            layer = self.tagger.make_layer(text, layers)
            if 'output_layer' in content.keys():
                layer.name = content['output_layer']
            # No need to do layer_to_json: Response obj will handle the conversion
            return Response(layer_to_dict(layer), mimetype="application/json")
        except ValidationError as error:
            return Response(content=error.messages, http_status_code=400)
        except ValueError as err:
            # If tagger.make_layer throws a ValueError, report about a missing layer
            return Response(content='Error at input processing: {}'.format(str(err)), http_status_code=400)
        except Exception as error:
            return Response(content='Internal error at input processing', http_status_code=400)


if __name__ == "__main__":
    worker = NeuralMorphTaggerWorker(model_dir=settings.MODEL_PATH)
    worker.start(connection_parameters=settings.MQ_PARAMS,
                 service_name=settings.SERVICE_NAME,
                 routing_key=settings.ROUTING_KEY)
