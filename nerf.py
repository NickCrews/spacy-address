""".nerf is a domain specific schema of JSON for annotating NER data.

I made it up for this project. It looks like this:

[
  {
    "text": "431 Marietta St NW Fl. 3",
    "ents": [
      {
        "text": "431",
        "label": "AddressNumber"
      },
      {
        "text": "Marietta",
        "label": "StreetName"
      },
      {
        "text": "St",
        "label": "StreetNamePostType"
      },
      {
        "text": "NW",
        "label": "StreetNamePostDirectional"
      },
      {
        "text": "Fl.",
        "label": "OccupancyType"
      },
      {
        "text": "3",
        "label": "OccupancyIdentifier",
        "start": 23,
        "end": 24
      }
    ]
  },
  {
    "text": "1234 West U.S. Hwy 50",
    "ents": [
      {
        "text": "1234",
        "label": "AddressNumber"
      },
      {
        "text": "West",
        "label": "StreetNamePreDirectional"
      },
      {
        "text": "U.S. Hwy",
        "label": "StreetNamePreType"
      },
      {
        "text": "50",
        "label": "StreetName"
      }
    ]
  },
...

Each document is a dictionary with a text key and a list of entities.
If the text of an entity is unique in the document,
we can define its location just using the text.
If it is in there multiple times, we need to use the start and end indices.

I chose this format because I think it is optimized for readability
and ease of editing by hand. It may change at any time, don't rely on it.
I thought about using something less computer-readable like

431 Marietta St NW Fl. 3
  431 AddressNumber
  Marietta StreetName
  St StreetNamePostType
  NW StreetNamePostDirectional
  Fl. OccupancyType
  3 OccupancyIdentifier 23 24

But I was running into issues with being able to include newlines in the text.
This json method is also way easier to serialize and deserialize.

Included in this module are utils to convert to and from spaCy's Docs and DocBins.
"""

import dataclasses
import json
from pathlib import Path
from typing import Iterable

import spacy
import typer
from spacy.tokens import Doc, DocBin, Span


@dataclasses.dataclass(kw_only=True, frozen=True)
class EntSpec:
    """Specifies an entity in a document.

    If the entity is in the document only once, we can define its location only using the text.
    If it is in there multiple times, we need to use the start and end.
    """

    text: str
    label: str
    start: int | None = None
    end: int | None = None

    @classmethod
    def from_span(cls, span: Span):
        doc = span.doc
        if doc.text.count(span.text) == 1:
            start = None
            end = None
        else:
            start = span.start_char
            end = span.end_char
        return cls(label=span.label_, text=span.text, start=start, end=end)

    def to_span(self, doc: Doc) -> Span:
        if self.start is None:
            start = doc.text.index(self.text)
            end = start + len(self.text)
        else:
            start = self.start
            end = self.end
        return doc.char_span(start, end, label=self.label)

    def to_dict(self) -> dict:
        d = {
            "text": self.text,
            "label": self.label,
        }
        if self.start is not None:
            d["start"] = self.start
            d["end"] = self.end
        return d


@dataclasses.dataclass
class DocSpec:
    text: str
    ents: list[EntSpec]

    def to_doc(self, nlp: spacy.Language) -> Doc:
        doc = nlp.make_doc(self.text)
        for ent in self.ents:
            doc.ents = list(doc.ents) + [ent.to_span(doc)]
        return doc

    @classmethod
    def from_doc(cls, doc: Doc):
        ents = [EntSpec.from_span(span) for span in doc.ents]
        return cls(doc.text, ents)

    def to_dict(self) -> dict:
        return {"text": self.text, "ents": [ent.to_dict() for ent in self.ents]}

    @classmethod
    def from_dict(cls, d: dict) -> "DocSpec":
        ents = [EntSpec(**ent) for ent in d["ents"]]
        return cls(d["text"], ents)


def docspecs_to_nerf(specs: Iterable[DocSpec], path: Path):
    """Convert DocSpecs to a .nerf file."""
    spec_dicts = [spec.to_dict() for spec in specs]
    with path.open("w") as file_:
        json.dump(spec_dicts, file_, indent=2)


def nerf_to_docspecs(path: Path) -> Iterable[DocSpec]:
    # pattern = re.compile(r"^ (.+) ([a-zA-Z]+\S*)(?: (\d+) (\d+))?$")
    with path.open() as file_:
        spec_dicts = json.load(file_)
        return [DocSpec.from_dict(d) for d in spec_dicts]


def docspecs_to_docbin(
    specs: Iterable[DocSpec], nlp: spacy.Language | None = None
) -> DocBin:
    if nlp is None:
        nlp = spacy.blank("en")
    doc_bin = DocBin()
    for spec in specs:
        doc = spec.to_doc(nlp)
        doc_bin.add(doc)
    return doc_bin


def docbin_to_docspecs(doc_bin: DocBin) -> Iterable[DocSpec]:
    nlp = spacy.blank("en")
    for doc in doc_bin.get_docs(nlp.vocab):
        yield DocSpec.from_doc(doc)


def docbin_to_nerf(docbin: DocBin, nerf_path: Path):
    specs = docbin_to_docspecs(docbin)
    docspecs_to_nerf(specs, nerf_path)


def nerf_to_docbin(nerf_path: Path) -> DocBin:
    specs = nerf_to_docspecs(nerf_path)
    return docspecs_to_docbin(specs)


def cli(
    inp: str,
    out: str,
    inp_format: str | None = None,
    out_format: str | None = None,
):
    """Convert between .nerf and .spacy files."""
    inp_path = Path(inp)
    out_path = Path(out)

    if inp_format is None:
        inp_format = inp_path.suffix.lstrip(".")
    if out_format is None:
        out_format = out_path.suffix.lstrip(".")

    if inp_format not in ["spacy", "nerf"]:
        raise ValueError(f"Invalid input format: {inp_format}")
    if out_format not in ["spacy", "nerf"]:
        raise ValueError(f"Invalid output format: {out_format}")

    if inp_format == "spacy" and out_format == "nerf":
        docbin = DocBin().from_disk(inp_path)
        docbin_to_nerf(docbin, out_path)
    elif inp_format == "nerf" and out_format == "spacy":
        docbin = nerf_to_docbin(inp_path)
        docbin.to_disk(out_path)
    else:
        raise ValueError(f"Cannot convert from {inp_format} to {out_format}")


if __name__ == "__main__":
    typer.run(cli)
