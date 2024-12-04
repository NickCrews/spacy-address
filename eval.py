"""Visualize the bad predictions of a NER model using streamlit.

streamlit run eval.py
"""

from pathlib import Path
from typing import Iterable

import spacy
import streamlit as st
import typer
from spacy.tokens import DocBin
from spacy.training import Example
from spacy_streamlit import visualize_ner


def load_examples(
    nlp: spacy.Language | Path | None = None,
    doc_bin: DocBin | Path | None = None,
) -> list[Example]:
    if nlp is None:
        nlp = Path("./models/sm/training/model-last")
    if isinstance(nlp, Path):
        nlp = spacy.load(nlp)

    if doc_bin is None:
        doc_bin = Path("./data/dev.spacy")
    if isinstance(doc_bin, Path):
        doc_bin = DocBin().from_disk(doc_bin)

    doc_bin = doc_bin.get_docs(nlp.vocab)
    return [Example(nlp(reference.text), reference) for reference in doc_bin]


def is_misprediction(example: Example) -> bool:
    labels_ref = [ent.label_ for ent in example.reference.ents]
    labels_pred = [ent.label_ for ent in example.predicted.ents]
    return labels_ref != labels_pred


def viz_examples(examples: Iterable[Example]):
    st.set_page_config(layout="wide")
    for i, ex in enumerate(examples):
        if not is_misprediction(ex):
            continue
        col1, col2 = st.columns(2)
        with col1:
            visualize_ner(
                ex.reference,
                show_table=False,
                key=f"{i}_ref",
                title="Reference",
            )
        with col2:
            visualize_ner(
                ex.predicted,
                show_table=False,
                key=f"{i}_pred",
                title="Predicted",
            )


def main(nlp: None | Path = None, docbin: None | Path = None):
    examples = load_examples(nlp, docbin)
    viz_examples(examples)


if __name__ == "__main__":
    typer.run(main)
