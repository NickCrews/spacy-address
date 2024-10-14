from types import ModuleType

import spacy


def test_package_name(package: ModuleType):
    package_name = package.__name__.split(".")[-1]
    assert package_name.startswith("en_us_address_ner_")


def test_labels(package: ModuleType):
    assert isinstance(package.labels.AddressNumber, str)


def test_loadable(package: ModuleType):
    assert isinstance(package.load(), spacy.language.Language)


def test_inference(package: ModuleType):
    nlp = package.load()
    doc = nlp("CO John SMITH, 123 E St elias stree S,   Oklahoma City, OK 99507-1234")
    expected = [
        ("CO John SMITH", "Recipient"),
        ("123", "AddressNumber"),
        ("E", "StreetNamePreDirectional"),
        ("St elias", "StreetName"),
        ("stree", "StreetNamePostType"),
        ("S", "StreetNamePostDirectional"),
        ("Oklahoma City", "PlaceName"),
        ("OK", "StateName"),
        ("99507-1234", "ZipCode"),
    ]
    actual = [(ent.text, ent.label_) for ent in doc.ents]
    assert actual == expected
