"""
Converts XML data to spacy binary format.

The [raw data from usaddress](https://github.com/datamade/usaddress/blob/a42a8f0c14bd2e273939fd51c604f10826301e73/training/labeled.xml
is in XML.
spaCy expects it in it's own proprietary binary format.

Raw data looks like:
<AddressCollection>
  <AddressString><AddressNumber>8128</AddressNumber> <StreetNamePreDirectional>S.</StreetNamePreDirectional> <StreetName>DR</StreetName> <StreetName>MARTIN</StreetName> <StreetName>LUTHER</StreetName> <StreetName>KING</StreetName> <StreetName>JR</StreetName> <StreetNamePostType>Drive</StreetNamePostType></AddressString>
  <AddressString><AddressNumber>3600</AddressNumber> <StreetNamePreDirectional>West</StreetNamePreDirectional> <StreetName>5th</StreetName> <StreetNamePostType>Ave</StreetNamePostType></AddressString>
"""
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "spacy",
# ]
# ///

import argparse
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Iterable, NamedTuple

import spacy
from spacy.tokens import Doc, DocBin, Span


class Token(NamedTuple):
    text: str
    label: str


def xml_to_token_lists(path):
    root = ET.parse(path).getroot()
    for doc in root:
        # strip because some raw text has leading/trailing spaces, which spacy can't handle
        yield [Token(token.text.strip(), token.tag) for token in doc]


def tokens_to_doc(tokens: Iterable[Token], nlp: spacy.language.Language) -> Doc:
    tokens = list(tokens)
    doc = nlp.make_doc(" ".join(token.text for token in tokens))
    spans = list(tokens_to_entities(tokens, doc))
    # print("==========")
    # print(doc)
    # for span in spans:
    #     print(span, span.start, span.end, span.label_)
    # print("==========")
    doc.ents = spans
    return doc


def tokens_to_entities(tokens: Iterable[Token], doc: Doc) -> Iterable[Span]:
    """Merge tokens into spans of the same label.

    If consecutive tokens have the same label, they are merged into a single span.
    Tokens can have trailing commas from the messy raw data, so we strip them from
    the entity text.
    """
    start = 0
    text = ""
    label = None
    for token in tokens:
        if label is None:
            label = token.label
            text = token.text
            continue
        if token.label == label:
            text += " " + token.text
            continue
        yield doc.char_span(start, start + len(text.removesuffix(",")), label=label)

        start += len(text) + 1
        label = token.label
        text = token.text
    if text:
        yield doc.char_span(start, start + len(text.removesuffix(",")), label=label)


def token_lists_to_docbin(
    token_lists: Iterable[Iterable[Token]], nlp: spacy.language.Language
) -> DocBin:
    return DocBin(docs=[tokens_to_doc(tokens, nlp) for tokens in token_lists])


def convert(input_path, output_path):
    token_lists = list(xml_to_token_lists(input_path))
    nlp = spacy.blank("en")
    db = token_lists_to_docbin(token_lists, nlp)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    db.to_disk(output_path)


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path")
    parser.add_argument("output_path")
    args = parser.parse_args()
    convert(args.input_path, args.output_path)


if __name__ == "__main__":
    cli()
