# Gene-Ontology-Analyser

Automatically group genes according to ontology data

## Usage

Download with:
```
git clone https://github.com/phenotypic/Gene-Ontology-Analyser.git
pip3 install -r requirements.txt
```

Run from the same directory with:
```
python3 analyse.py
```

Here are some flags you can add:

| Flag | Description |
| --- | --- |
| `-s <subset>` | Subset: Define a [GO subset](https://github.com/geneontology/go-ontology/tree/master/src/ontology/subsets), read more [here](http://geneontology.org/docs/go-subset-guide/) (default: `goslim_agr`) |
| `-n` | Names: Retrieve new HGNC ids for symbols.txt file |
| `-r` | Names: Retrieve new ontology data from API |
