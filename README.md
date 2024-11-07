# spacy-address

Use [spaCy](https://spacy.io/)'s NER pipeline to parse oneline US addresses

Uses the the labeled data from [usaddress](https://github.com/datamade/usaddress)
with spaCy's very easy [training infrastructure](https://spacy.io/usage/training)

Inspired by the code and blog from https://github.com/swapnil-saxena/address-parser.

## Usage

There are currently two models, `en-us-address-ner-sm` and `en-us-address-ner-lg`,
following the naming conventions for small and large that spaCy uses.

### en-us-address-ner-sm

You probably want this one. Much better efficiency for not much worse accuracy.

As of 2024-10-06:

- F1 score for NER of .978
- model size of ~5MB
- on my 2021 M1 MacBook Pro, tags 1000 addresses in ~.2 sec

### en-us-address-ner-lg

Much larger and slower, a little more accurate.

As of 2024-10-06:

- F1 score for NER of .982
- model size of ~420MB
- on my 2021 M1 MacBook Pro, tags 1000 addresses in ~2 sec

You can find the released models in various [github releases](https://github.com/NickCrews/spacy-address/releases).
There, you can see the most up to date model size and F1 score.
The speed isn't reported anywhere easily, unfortunately.

You can install from a release directly with pip:

```bash
python -m pip install "en-us-address-ner-sm @ https://github.com/NickCrews/spacy-address/releases/download/20241029-205717-sm/en_us_address_ner_sm-0.0.0-py3-none-any.whl"
```

Now, this is accessible from python:

```python
import spacy

nlp = spacy.load("en-us-address-ner-sm")
doc = nlp("CO John SMITH, 123 E St elias stree S,   Oklahoma City, OK 99507-1234")
for ent in doc.ents:
    print(f"{ent.text} ({ent.label_})")
# CO John SMITH (Recipient)
# 123 (AddressNumber)
# E (StreetNamePreDirectional)
# St elias (StreetName)            # St isn't confused as an abbreviation for street!
# stree (StreetNamePostType)       # Typos are tagged correctly!
# S (StreetNamePostDirectional)
# Oklahoma City (PlaceName)        # Oklahoma isn't confused as a state!
# OK (StateName)
# 99507-1234 (ZipCode)

# For convenience I include the taggings for autcomplete, IDE support, etc
from en_us_address_ner_sm import labels
[ent.text for ent in doc.ents if ent.label_ == labels.StateName]
# ['OK']
```

This uses the tags from the
"United States Thoroughfare, Landmark, and Postal Address Data Standard (Publication 28)".
See [labels.py](./labels.py) for details

## Goals

I have tried using various probabilstic address parsers/taggers. None of them
quite suited my needs. Here is what I was aiming for

- Speed: I am doing bulk processing, I want to parse 10s of millions of addresses in <5 minutes
- Support for PO Boxes.
- Support for finegrained tagging, eg split "Aspen Avenue" into ("Aspen", StreetName), ("Avenue", StreetPostType).
  I need this for performing entity resolution, I only really care about the street name.
- Python API
- An installation story that isn't a total pain.

Here is an incomplete list of how this project compares with some other projects
I've tried:

## Comparison vs Peers

### [Libpostal](https://github.com/openvenues/libpostal)

- appears fairly unmaintained. It still works, but mostly all development
appears to keep the lights on.
- pain in the butt to deploy. You have to build from source using git, gcc, no `pip`.
- Requires a few GB of data (this amount might not be totally correct, but anyways a lot)
- it's not thread safe, and hard to integrate with other projects.
See https://github.com/Maxxen/duckdb-postal/issues/1
- Uses OpenStreetMap, with addresses from around the world
- Uses [a slightly different set of tags](https://github.com/OpenCageData/address-formatting)
from this project. They are less USPS-specific, more applicable for worldwide addresses,
but aren't as granular, ie we tag "NW" as a StreetPreDirectional, they don't
go to that level of detail. We tag post office boxes and rural routes, they don't.
Might be more differences than what I have here. I'm open to expanding to a different
tagging scheme, but I NEED to support USPS PO box tagging, and of separating out the
street name ("Aspen") vs street type ("Avenue").
- According to [their very in depth blog post](https://medium.com/@albarrentine/statistical-nlp-on-openstreetmap-b9d573e6cc86),
it's quite more technically specialized than the other solutions here.
Does a lot of hand-written, address-domain specific things like normalizing st -> street,
hand-parsing numbers with custom grammar rules, etc.
- uses something called a "averaged perceptron" which they claim is much faster than
 conditional random fields (as usaddress uses). IDK what spacy is doing...
- I would be very interested in a speed comparison vs us, building a c app
that does bulk processing.
- They claim a ~99.5% accuracy, which is similar to what we achieve.
I would love to test this though.

### [PyPostal](https://github.com/openvenues/pypostal)
The python bindings to libpostal.
- has same installation problems as the above.
- only provides a one-by-one inference API, no batch API
- I would be very interested in a speed comparison vs us.

### [USAddress](https://github.com/datamade/usaddress)
- Python only. Installable with `pip`!
- Not actively maintained, but basic maintenance happens.
- Older architecture (conditional random fields, but that doesn't mean anything to me...)
- Uses same set of taggings as us.
- Also uses OpenStreetMap data.
- Tokenizes in python using hardcoded rules. in spacy, the tokenizer is another trained model.
  IDK really the consequences of this.
- I would be very interested in a speed comparison vs us.
- IDK what their accuracy numbers are.

## Licence

Released under the MIT license.