# fastapi-entity-detection

This repository has the `fastAPI` code for entity detection in a sentence. The `model.py` code utilizes spacy pretrained pipeline to identify entities which are by default detected by spacy as well as a custom entities such as **name, phone no., email id, blood group, date, url** using rule based entity detection.

Note - The rule based entity detection used in the model.py is not perfect but it can detect tag the custom entities to some point. This can be solved by training the spacy-pipline for custom entities.
