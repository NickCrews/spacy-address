train:
    python xml2spacy.py data/train.xml data/train.spacy
    python xml2spacy.py data/test.xml data/test.spacy
    python -m spacy train config.cfg --output ./training --paths.train ./data/train.spacy --paths.dev ./data/test.spacy

# Convert the trained model to a python package
package:
    python -m spacy package training/model-best packages --build wheel --force --name us_address_ner

# Publish the python package to GitHub releases
release:
    gh release create $(date -u '+%Y%m%d-%H%M%S') packages/en_*/dist/*.whl --title "Release $(date -u '+%Y%m%d-%H%M%S')" --generate-notes

# Fetch the labeled XML data from the usaddress repository
fetch-data:
    curl https://raw.githubusercontent.com/datamade/usaddress/refs/heads/main/training/labeled.xml > data/train.xml
    curl https://raw.githubusercontent.com/datamade/usaddress/refs/heads/main/measure_performance/test_data/labeled.xml > data/test.xml
    curl https://raw.githubusercontent.com/EthanRBrown/rrad/refs/heads/master/addresses-us-1000.json > data/benchmark.json
