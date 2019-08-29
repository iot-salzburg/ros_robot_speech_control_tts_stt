import io
import json

from snips_nlu import SnipsNLUEngine
from snips_nlu.default_configs import CONFIG_EN #For German please use ..._DE

engine = SnipsNLUEngine(config=CONFIG_EN)

with io.open("dataset.json") as f: #dataset.json needs to be changed to the JSON you generated via YAML
    dataset = json.load(f)

engine.fit(dataset)
engine.persist("path/to/directory")