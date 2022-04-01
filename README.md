# scriptscz

```mermaid
flowchart LR
    A[Transformer Language Models] --> B{Does it have Encoder Transformer?}
    B -- Yes --> C[Does it also have Decoder Transformer?]
    C -- Yes ----> D[T5] ----> G{cross entropy loss}
    G --> J{static} 
    G --> K{moving window}
    D ----> P{cosine similarity}
    P --> Q{word embeddings}
    P --> R{utterance embeddings}
    C -- No ----> E[BERT] ----> H{probability logits}
    H --> L{static} 
    H --> M{moving window}
    E ----> S{cosine similarity}
    S --> T{word embeddings}
    S --> U{utterance embeddings}
    B -- No ----> F[GPT] ----> I{perplexity}
    I --> N{stride = 3}
    I --> O{stride > 3}
    F ----> V{cosine similarity}
    V --> W{word embeddings}
    V --> X{utterance embeddings}
    click A "https://github.com/yancong222/scriptscz/blob/main/perplexity/ed_perplexity.py" _blank
    click B "http://www.github.com" "Open this in a new tab" _blank
    click C href "http://www.github.com" _blank
    click D href "http://www.github.com" "Open this in a new tab" _blank
```
---------------------------------------------

This folder contains various scripts and modified code (Python, R, shell) written or adapted by Yan Cong starting in August 2021 at The Feinstein Institutes for Medical Research.

There are five subfolders, each representing a different study. Each subfolder contains its own Readme file with a summary of the contents of that folder.

---------------------------------------------

The "classifiers" subfolder: build classifiers to capture speech disorganizations

The "ner" subfolder: name entity recognition in text files

The "pdtb" subfolder: use penn-discourse-treebank parser to annotate discourse relations

The "perplexity" subfolder: use transformers' perplexity metrics to understand speech incoherence

The "similarity" subfolder: use transformers' similarity metrics to understand speech inefficiency


