# Webservice for EstNLTK's neural morphological tagger / disambiguator

### Setting up the model

Before setting up the web service, you need to obtain the model. You can download model files from [`https://s3.hpc.ut.ee/estnltk/estnltk_resources/neural_morph_softmax_emb_cat_sum_2019-08-23.zip`](https://s3.hpc.ut.ee/estnltk/estnltk_resources/neural_morph_softmax_emb_cat_sum_2019-08-23.zip). Unpack the zipped content of `/neural_morph_disamb/softmax_emb_cat_sum_23-08-2019/output/` into local directory `softmax_emb_cat_sum/output/`. After all necessary model files have been assembled, the local directory  `softmax_emb_cat_sum` should have the following structure:

		softmax_emb_cat_sum/
		├── __init__.py
		├── config.py
		├── config_holder.py
		├── general_utils.py
		├── model.py
		├── neural_morph_logger.py
		├── output
		│   ├── data
		│   │   ├── analysis.txt
		│   │   ├── chars.txt
		│   │   ├── embeddings.npz
		│   │   ├── singletons.txt
		│   │   ├── tags.txt
		│   │   └── words.txt
		│   ├── readme.md
		│   └── results
		│       ├── log.txt
		│       ├── model.weights.data-00000-of-00001
		│       ├── model.weights.index
		│       └── model.weights.meta
		└── rnn_util.py

### Configuration

The configuration follows the configuration used in https://github.com/liisaratsep/berttaggernazgul.

The Docker image can be built with 3 configurations that can be defined by a build argument NAURON_MODE. By default, the image contains a Gunicorn + Flask API running `SoftmaxEmbCatSumTagger`. The `GATEWAY` configuration creates an image that only contains the API which posts requests to a RabbitMQ message queue server. The `WORKER` configuration creates a worker that picks up requests from the message queue and processes them.

The RabbitMQ server configuration can be defined with environment variables `MQ_HOST`, `MQ_PORT`, `MQ_USERNAME` and `MQ_PASSWORD`. The web server can be configured with the default Gunicorn parameters by using the `GUNICORN_` prefix.

Docker compose configuration to run separate a gateway and worker containers with RabbitMQ:

TODO

### Quick testing of the webservice

To quickly test if the webservice has been set up properly and appears to run OK, try the following `curl` query:

    curl http://127.0.0.1:5000/estnltk/tagger/neural_morph_disamb -H "Content-Type: application/json" -d '{"text": "Ilus suur karvane kass nurrus rohelisel diivanil.", "meta": {}, "layers": "{\"sentences\": {\"name\": \"sentences\", \"attributes\": [], \"parent\": null, \"enveloping\": \"words\", \"ambiguous\": false, \"serialisation_module\": null, \"meta\": {}, \"spans\": [{\"base_span\": [[0, 4], [5, 9], [10, 17], [18, 22], [23, 29], [30, 39], [40, 48], [48, 49]], \"annotations\": [{}]}]}, \"compound_tokens\": {\"name\": \"compound_tokens\", \"attributes\": [\"type\", \"normalized\"], \"parent\": null, \"enveloping\": \"tokens\", \"ambiguous\": false, \"serialisation_module\": null, \"meta\": {}, \"spans\": []}, \"tokens\": {\"name\": \"tokens\", \"attributes\": [], \"parent\": null, \"enveloping\": null, \"ambiguous\": false, \"serialisation_module\": null, \"meta\": {}, \"spans\": [{\"base_span\": [0, 4], \"annotations\": [{}]}, {\"base_span\": [5, 9], \"annotations\": [{}]}, {\"base_span\": [10, 17], \"annotations\": [{}]}, {\"base_span\": [18, 22], \"annotations\": [{}]}, {\"base_span\": [23, 29], \"annotations\": [{}]}, {\"base_span\": [30, 39], \"annotations\": [{}]}, {\"base_span\": [40, 48], \"annotations\": [{}]}, {\"base_span\": [48, 49], \"annotations\": [{}]}]}, \"words\": {\"name\": \"words\", \"attributes\": [\"normalized_form\"], \"parent\": null, \"enveloping\": null, \"ambiguous\": true, \"serialisation_module\": null, \"meta\": {}, \"spans\": [{\"base_span\": [0, 4], \"annotations\": [{\"normalized_form\": null}]}, {\"base_span\": [5, 9], \"annotations\": [{\"normalized_form\": null}]}, {\"base_span\": [10, 17], \"annotations\": [{\"normalized_form\": null}]}, {\"base_span\": [18, 22], \"annotations\": [{\"normalized_form\": null}]}, {\"base_span\": [23, 29], \"annotations\": [{\"normalized_form\": null}]}, {\"base_span\": [30, 39], \"annotations\": [{\"normalized_form\": null}]}, {\"base_span\": [40, 48], \"annotations\": [{\"normalized_form\": null}]}, {\"base_span\": [48, 49], \"annotations\": [{\"normalized_form\": null}]}]}, \"morph_analysis\": {\"name\": \"morph_analysis\", \"attributes\": [\"normalized_text\", \"lemma\", \"root\", \"root_tokens\", \"ending\", \"clitic\", \"form\", \"partofspeech\"], \"parent\": \"words\", \"enveloping\": null, \"ambiguous\": true, \"serialisation_module\": null, \"meta\": {}, \"spans\": [{\"base_span\": [0, 4], \"annotations\": [{\"normalized_text\": \"Ilus\", \"lemma\": \"ilus\", \"root\": \"ilus\", \"root_tokens\": [\"ilus\"], \"ending\": \"0\", \"clitic\": \"\", \"form\": \"sg n\", \"partofspeech\": \"A\"}]}, {\"base_span\": [5, 9], \"annotations\": [{\"normalized_text\": \"suur\", \"lemma\": \"suur\", \"root\": \"suur\", \"root_tokens\": [\"suur\"], \"ending\": \"0\", \"clitic\": \"\", \"form\": \"sg n\", \"partofspeech\": \"A\"}]}, {\"base_span\": [10, 17], \"annotations\": [{\"normalized_text\": \"karvane\", \"lemma\": \"karvane\", \"root\": \"karvane\", \"root_tokens\": [\"karvane\"], \"ending\": \"0\", \"clitic\": \"\", \"form\": \"sg n\", \"partofspeech\": \"A\"}]}, {\"base_span\": [18, 22], \"annotations\": [{\"normalized_text\": \"kass\", \"lemma\": \"kass\", \"root\": \"kass\", \"root_tokens\": [\"kass\"], \"ending\": \"0\", \"clitic\": \"\", \"form\": \"sg n\", \"partofspeech\": \"S\"}]}, {\"base_span\": [23, 29], \"annotations\": [{\"normalized_text\": \"nurrus\", \"lemma\": \"nurruma\", \"root\": \"nurru\", \"root_tokens\": [\"nurru\"], \"ending\": \"s\", \"clitic\": \"\", \"form\": \"s\", \"partofspeech\": \"V\"}]}, {\"base_span\": [30, 39], \"annotations\": [{\"normalized_text\": \"rohelisel\", \"lemma\": \"roheline\", \"root\": \"roheline\", \"root_tokens\": [\"roheline\"], \"ending\": \"l\", \"clitic\": \"\", \"form\": \"sg ad\", \"partofspeech\": \"A\"}]}, {\"base_span\": [40, 48], \"annotations\": [{\"normalized_text\": \"diivanil\", \"lemma\": \"diivan\", \"root\": \"diivan\", \"root_tokens\": [\"diivan\"], \"ending\": \"l\", \"clitic\": \"\", \"form\": \"sg ad\", \"partofspeech\": \"S\"}]}, {\"base_span\": [48, 49], \"annotations\": [{\"normalized_text\": \".\", \"lemma\": \".\", \"root\": \".\", \"root_tokens\": [\".\"], \"ending\": \"\", \"clitic\": \"\", \"form\": \"\", \"partofspeech\": \"Z\"}]}]}}", "output_layer": "neural_morph_disamb"}'


Expected result:

    {"ambiguous":false,"attributes":["morphtag","pos","form"],"enveloping":null,"meta":{},"name":"neural_morph_disamb","parent":"words","serialisation_module":null,"spans":[{"annotations":[{"form":"sg n","morphtag":"POS=A|DEGREE=pos|NUMBER=sg|CASE=nom","pos":"A"}],"base_span":[0,4]},{"annotations":[{"form":"sg n","morphtag":"POS=A|DEGREE=pos|NUMBER=sg|CASE=nom","pos":"A"}],"base_span":[5,9]},{"annotations":[{"form":"sg n","morphtag":"POS=A|DEGREE=pos|NUMBER=sg|CASE=nom","pos":"A"}],"base_span":[10,17]},{"annotations":[{"form":"sg n","morphtag":"POS=S|NOUN_TYPE=com|NUMBER=sg|CASE=nom","pos":"S"}],"base_span":[18,22]},{"annotations":[{"form":"s","morphtag":"POS=V|VERB_TYPE=main|MOOD=indic|TENSE=impf|PERSON=ps3|NUMBER=sg|VERB_PS=ps|VERB_POLARITY=af","pos":"V"}],"base_span":[23,29]},{"annotations":[{"form":"sg ad","morphtag":"POS=A|DEGREE=pos|NUMBER=sg|CASE=ad","pos":"A"}],"base_span":[30,39]},{"annotations":[{"form":"sg ad","morphtag":"POS=S|NOUN_TYPE=com|NUMBER=sg|CASE=ad","pos":"S"}],"base_span":[40,48]},{"annotations":[{"form":"","morphtag":"POS=Z|PUNCT_TYPE=Fst","pos":"Z"}],"base_span":[48,49]}]}