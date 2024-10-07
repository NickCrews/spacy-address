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
python -m pip install "en-us-address-ner-sm @ https://github.com/NickCrews/spacy-address/releases/download/20241007-072524-sm/en_us_address_ner_sm-0.0.0-py3-none-any.whl"
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
```

This uses the tags from the
"United States Thoroughfare, Landmark, and Postal Address Data Standard (Publication 28)":
- AddressNumber
- AddressNumberPrefix
- AddressNumberSuffix
- BuildingName
- CornerOf
- CountryName
- IntersectionSeparator
- LandmarkName
- NotAddress
- OccupancyIdentifier
- OccupancyType
- PlaceName
- Recipient
- StateName
- StreetName
- StreetNamePostDirectional
- StreetNamePostModifier
- StreetNamePostType
- StreetNamePreDirectional
- StreetNamePreModifier
- StreetNamePreType
- SubaddressIdentifier
- SubaddressType
- USPSBoxGroupID
- USPSBoxGroupType
- USPSBoxID
- USPSBoxType
- ZipCode
- ZipPlus

## Licence

Released under the MIT license.