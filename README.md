# spacy-address

Use [spaCy](https://spacy.io/)'s NER pipeline to parse oneline US addresses

Uses the the labeled data from [usaddress](https://github.com/datamade/usaddress)
with spaCy's very easy [training infrastructure](https://spacy.io/usage/training)

Inspired by the code and blog from https://github.com/swapnil-saxena/address-parser.

## Install

I will try to improve the package name a bit, but here is something that currently works:

```bash
python -m pip install "en-us-address-ner @ https://github.com/NickCrews/spacy-address/releases/download/20241006-233052/en_us_address_ner-0.0.0-py3-none-any.whl"
```

Now, this is accessible from python:

```python
import spacy

nlp = spacy.load("en-us-address-ner")
doc = nlp("123 E Elm st S,   Oklahoma City, OK 99507-1234")
for ent in doc.ents:
    print(ent.text, ent.label_)
# 123 AddressNumber
# E StreetNamePreDirectional
# Elm StreetName
# st StreetNamePostType
# S, StreetNamePostDirectional
# Oklahoma PlaceName             # nice, this is recognized as a place, not a state!
# City, PlaceName
# OK StateName
# 99507-1234 ZipCode
```

On my 2021 M1 Macbook Pro with 64GB of RAM, it takes ~2 seconds to parse 1000 addresses.

This uses the tags that the us postal service uses (need to track down the exact reference):
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

## Future Work

- Currently the pipeline is based on the `en_core_web_lg` model. I want to make variations
  that are based on the `en_core_web_sm` for faster inference, and the `en_core_web_trf`
  for best performance
- Improve the metadata that is included in the released packages.
  Something to do with the `meta.json` file that is used in the `spacy package` command?

## Licence

Released under the MIT license.