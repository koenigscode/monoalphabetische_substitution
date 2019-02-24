from tkinter import (Text, END)


def write_to_text(text: Text, string: str) -> None:
    """Deletes text of Text Widget and fills it with string param"""
    text.delete(1.0, END)
    text.insert("end", string)
    text.see("end")


def replace_char(mapping_dict: dict, c: str) -> tuple:
    """Maps one character to another"""
    return (True, mapping_dict[c]) if c in mapping_dict and mapping_dict[c] else (False, c)


def create_mapping_dict(labels: dict, mapping: list) -> dict:
    """Creates mapping dictionary from labels and entries"""
    return {from_label(labels, lbl["text"]): ent.get() for lbl, ent in mapping}


def to_label(labels: dict, c: str) -> str:
    return labels[c] if c in labels and labels[c] else c


def from_label(labels: dict, c: str) -> str:
    rev_char_labels = {v: k for k, v in labels.items()}
    return rev_char_labels[c] if c in rev_char_labels and rev_char_labels[c] else c
