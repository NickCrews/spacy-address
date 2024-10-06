train:
    python -m spacy train config.cfg --output ./output --paths.train ./data/train.spacy --paths.dev ./data/test.spacy

# Fetch the labeled XML data from the usaddress repository
fetch-data:
    curl https://raw.githubusercontent.com/datamade/usaddress/refs/heads/main/training/labeled.xml > data/train.xml
    curl https://raw.githubusercontent.com/datamade/usaddress/refs/heads/main/measure_performance/test_data/labeled.xml > data/test.xml

# Convert the labeled XML data to spaCy format
convert-data model='en_core_web_lg':
    python xml2spacy.py data/train.xml data/train.spacy  --model {{model}}
    python xml2spacy.py data/test.xml data/test.spacy --model {{model}}