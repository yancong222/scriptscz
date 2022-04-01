# scriptscz

```mermaid
flowchart LR
    A[Start] --> B{Does it have Encoder Transformer?}
    B -- Yes --> C[Does it also have Decoder Transformer?]
    C --> D[Yes] ----> F[T5]
    C --> E[No] ----> G[BERT]
    B -- No ----> H[GPT]
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


