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


def load_examples(nlp, dev_set):
    doc_bin = DocBin().from_disk(dev_set)
    docs = doc_bin.get_docs(nlp.vocab)
    return [Example(nlp(reference.text), reference) for reference in docs]


def viz_examples(examples: Iterable[Example]):
    st.set_page_config(layout="wide")
    for i, ex in enumerate(examples):
        labels_ref = [ent.label_ for ent in ex.reference.ents]
        labels_pred = [ent.label_ for ent in ex.predicted.ents]
        if labels_ref == labels_pred:
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


def main(
    nlp_dir: Path = "./models/sm/training/model-last",
    dev_set: Path = "./data/dev.spacy",
):
    nlp = spacy.load(nlp_dir)
    examples = load_examples(nlp, dev_set)
    viz_examples(examples)


if __name__ == "__main__":
    typer.run(main)
