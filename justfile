train model='sm':
    python xml2spacy.py data/train.xml data/train.spacy
    python xml2spacy.py data/test.xml data/test.spacy
    mkdir -p models/{{model}}/training
    python -m spacy train models/{{model}}/config.cfg --output models/{{model}}/training --paths.train ./data/train.spacy --paths.dev ./data/test.spacy

# Convert the trained model to a python package
package model='sm' version='model-best':
    mkdir -p models/{{model}}/package
    python -m spacy package models/{{model}}/training/{{version}} models/{{model}}/package --build wheel --force --meta-path models/{{model}}/meta.json

# Publish the python package to GitHub releases
release model='sm':
    gh release create $(date -u '+%Y%m%d-%H%M%S') models/{{model}}/packages/en_*/dist/*.whl --title "Release $(date -u '+%Y%m%d-%H%M%S')" --generate-notes

# Fetch the labeled XML data from the usaddress repository
fetch-data:
    curl https://raw.githubusercontent.com/datamade/usaddress/refs/heads/main/training/labeled.xml > data/train.xml
    curl https://raw.githubusercontent.com/datamade/usaddress/refs/heads/main/measure_performance/test_data/labeled.xml > data/test.xml
    curl https://raw.githubusercontent.com/EthanRBrown/rrad/refs/heads/master/addresses-us-1000.json > data/benchmark.json
