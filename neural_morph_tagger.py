#
#  This is a cut-down version of NeuralMorphTagger by Kermo Saarse and Kairit Sirts.
#  The original source can be found from estnltk_neural:
#  https://github.com/estnltk/estnltk/tree/9986ff7ae076e1874401b1869da462c2a53abd61/estnltk_neural/estnltk_neural/taggers/neural_morph/new_neural_morph
#

import importlib
import os, os.path

from estnltk_core import Layer, Tagger

from vabamorf_2_neural import neural_model_tags
from neural_2_vabamorf import vabamorf_tags

# =================================================================
#   Configuration handling
# =================================================================

def load_config_from_file(config_module_path):
    spec = importlib.util.spec_from_file_location("config", config_module_path)
    config = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config)
    return config

def get_model_path_from_dir(directory):
    """
    Checks if the given directory could contain NeuralMorphTagger's model.
    Returns path to the model's 'output' directory if a model directory 
    was found. Otherwise, returns None.
    """
    if directory is not None and os.path.isdir(directory):
        data_dir    = os.path.join(directory, 'output/data')
        results_dir = os.path.join(directory, 'output/results')
        if os.path.isdir(data_dir) and os.path.isdir(results_dir):
            # Model directory structure:
            #  output/data/*
            #  output/results/*
            return os.path.join(directory, 'output')
        else:
            dir_content = list(os.listdir(directory))
            if len(dir_content) == 1:
                subdir = dir_content[0]
                data_dir = \
                    os.path.join(directory, subdir+'/output/data')
                results_dir = \
                    os.path.join(directory, subdir+'/output/results')
                if os.path.isdir(data_dir) and \
                   os.path.isdir(results_dir):
                    # Model directory structure:
                    #  emb_cat_sum/output/data/*
                    #  emb_cat_sum/output/results/*
                    #  or 
                    #  emb_tag_sum/output/data/*
                    #  emb_tag_sum/output/results/*
                    return os.path.join(directory, subdir+'/output')
    # Expected structure not found ...
    return None

def override_config_paths_from_model_dir(config, model_dir):
    """
    Updates file paths in the configuration according to the 
    given model directory. 
    Note that the updating takes place only when given directory 
    is appropriate model directory, i.e. contains subfolders
    "output/data/*" and "output/results/*".
    Note also that this function does not check for the existence
    of model files.
    Returns config.
    """
    if isinstance(model_dir, str):
        out_dir = get_model_path_from_dir(model_dir)
        if out_dir is not None:
            # override configuration
            config.out_dir = out_dir
            config.out_dir = out_dir
            
            config.out_data_dir = os.path.join(out_dir, "data")
            config.dir_output = os.path.join(out_dir, "results")
            
            config.dir_model = os.path.join(config.dir_output, "model.weights")
            config.path_log = os.path.join(config.dir_output, "log.txt")
            config.training_log = os.path.join(config.dir_output, "training.log")
            
            config.filename_embeddings_trimmed = os.path.join(config.out_data_dir, "embeddings.npz")
            
            config.filename_words = os.path.join(config.out_data_dir, "words.txt")
            config.filename_tags = os.path.join(config.out_data_dir, "tags.txt")
            config.filename_chars = os.path.join(config.out_data_dir, "chars.txt")
            config.filename_analysis = os.path.join(config.out_data_dir, "analysis.txt")
            config.filename_singletons = os.path.join(config.out_data_dir, "singletons.txt")
    return config

MODEL_FILES = {"data": ["analysis.txt",
                        "chars.txt",
                        "embeddings.npz",
                        "singletons.txt",
                        "tags.txt",
                        "words.txt"],

               "results": ["model.weights.data-00000-of-00001",
                           "model.weights.index",
                           "model.weights.meta"]}


def check_model_files(model_dir):
    check_failed = False
    if os.path.exists(model_dir):
        for folder in MODEL_FILES:
            for file in MODEL_FILES[folder]:
                if not os.path.exists(os.path.join(model_dir, folder, file)):
                    check_failed = True
    else:
        check_failed = True
    if check_failed:
        msg = "Could not find model files from the location {!r}.".format(model_dir)
        raise FileNotFoundError( msg )

# =================================================================
#   Main
# =================================================================

class NeuralMorphTagger(Tagger):
    """Performs neural morphological tagging. It takes vabamorf analyses as input to predict
    morphological tags with better accuracy than vabamorf, but uses a different tag set.
    
    Do not use this class directly. Use the following methods to get taggers with
    different types of neural models:
        
    SoftmaxEmbTagSumTagger()
    SoftmaxEmbCatSumTagger()
    Seq2SeqEmbTagSumTagger()
    Seq2SeqEmbCatSumTagger()
    
    For example:
    
        text = Text("See on lause.")
        text.tag_layer(['morph_analysis'])
        
        tagger = SoftmaxEmbTagSumTagger()
        tagger.tag(text)
        
        print(text.neural_morph_analysis['morphtag'])
        
    Output:
        
        ['POS=P|NUMBER=sg|CASE=nom', 
         'POS=V|VERB_TYPE=main|MOOD=indic|TENSE=pres|PERSON=ps3|NUMBER=sg|VERB_PS=ps|VERB_POLARITY=af', 
         'POS=S|NOUN_TYPE=com|NUMBER=sg|CASE=nom', 
         'POS=Z|PUNCT_TYPE=Fst']

    """
    conf_param = ('model',)

    def __init__(self, output_layer='neural_morph_analysis', module_name=None, module_package=None,
                 model_module=None, model=None, model_dir=None):
        if module_name is not None:
            if module_package is not None:
                module_name = '.' + module_name
            model_module = importlib.import_module(module_name, module_package)
        if model_module is not None:
            module_path = os.path.dirname(model_module.__file__)
            config = load_config_from_file(os.path.join(module_path, "config.py"))
            if module_name is None:
                module_name = (model_module.__name__).split('.')[-1]
            else:
                assert (model_module.__name__).endswith(module_name)
            
            # Try to overwrite file paths in the configuration based on 
            # the given model directory. If model_dir is None, do nothing
            config = override_config_paths_from_model_dir(config, model_dir)

            check_model_files(config.out_dir)

            config_holder = model_module.ConfigHolder(config)
            self.model = model_module.Model(config_holder)
            self.model.build()
            self.model.restore_session(config.dir_model)
        else:
            self.model = model  # For unit testing

        self.output_layer = output_layer
        self.output_attributes = ('morphtag', 'pos', 'form')
        self.input_layers = ('morph_analysis', 'sentences', 'words')

    def _make_layer(self, text, layers, status=None):
        layer = Layer(name=self.output_layer,
                      text_object=text,
                      parent='words',
                      ambiguous=False,
                      attributes=self.output_attributes)
        morphtags = []

        for sentence in layers['sentences']:
            sentence_words = sentence.text
            analyses = []

            for word in sentence:
                word_text = word.text
                pos_tags = word.morph_analysis['partofspeech']
                forms = word.morph_analysis['form']

                word_analyses = []
                for pos, form in zip(pos_tags, forms):
                    word_analyses.extend(neural_model_tags(word_text, pos, form))
                analyses.append(word_analyses)

            morphtags.extend(self.model.predict(sentence_words, analyses))

        for word, tag in zip(layers['words'], morphtags):
            vm_pos, vm_form = vabamorf_tags(tag)
            layer.add_annotation(word, morphtag=tag, pos=vm_pos, form=vm_form)

        return layer

    def reset(self):
        self.model.reset()

class SoftmaxEmbCatSumTagger(NeuralMorphTagger):
    """SoftmaxEmbCatSumTagger
    """
    def __init__(self, output_layer: str = 'neural_morph_analysis', 
                       model_dir: str=os.path.join('softmax_emb_cat_sum','output')):
        super().__init__(output_layer=output_layer, module_name='softmax_emb_cat_sum',
                         module_package=None, model_dir=model_dir)



