# spacy-address

Use [spaCy](https://spacy.io/)'s NER pipeline to parse oneline US addresses

Uses the the labeled data from [usaddress](https://github.com/datamade/usaddress)
(which I think came from OSM data?)
with spaCy's very easy [training infrastructure](https://spacy.io/usage/training)

Still a work in progress. I've gotten `python -m spacy train` to run,
now still need to figure out how to publish or otherwise use this in production.

Released under the MIT license.