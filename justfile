# -1 to disable, eg `just gpu=-1 train`
gpu := '0'

train model='sm':
    python nerf.py data/train.nerf data/train.spacy
    python nerf.py data/dev.nerf data/dev.spacy
    mkdir -p models/{{model}}/training
    python -m spacy train models/{{model}}/config.cfg --output models/{{model}}/training --paths.train ./data/train.spacy --paths.dev ./data/dev.spacy  --gpu-id {{gpu}}

# Convert the trained model to a python package
package model='sm' version='model-best':
    mkdir -p models/{{model}}/package
    python -m spacy package models/{{model}}/training/{{version}} models/{{model}}/package --build wheel --force --meta-path models/{{model}}/meta.json --code labels.py

# Publish the python package to GitHub releases
release model='sm':
    gh release create $(date -u '+%Y%m%d-%H%M%S')-{{model}} models/{{model}}/package/*/dist/*.whl --title "Release $(date -u '+%Y%m%d-%H%M%S')-{{model}}" --notes-file models/{{model}}/package/*/README.md

# Fetch the labeled XML data from the usaddress repository
fetch-data:
    curl https://raw.githubusercontent.com/datamade/usaddress/refs/heads/main/training/labeled.xml > data/train.xml
    curl https://raw.githubusercontent.com/datamade/usaddress/refs/heads/main/measure_performance/test_data/labeled.xml > data/dev.xml
    curl https://raw.githubusercontent.com/EthanRBrown/rrad/refs/heads/master/addresses-us-1000.json > data/benchmark.json

test *ARGS:
    python -m pytest {{ARGS}}

# review the bad predictions
review:
    streamlit run eval.py