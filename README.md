# Gene-Ontology-Analyser

The script will sort a list of genes into groups within three [ontology subcategories](http://geneontology.org/docs/ontology-documentation/): `molecular funciton`, `biological process`, and `cellular component`.

First, the HGNC IDs for the input gene symbol list are retrieved using the [genenames.org](https://www.genenames.org) API. The [geneontology.org](http://api.geneontology.org/api) API is then used to retrieve all possible ontology categories for a specific [GO subset](http://geneontology.org/docs/go-subset-guide/), as well as the ontology ID list for each of the input genes. Finally, the script sorts the genes into ontological groups and outputs the data to `.csv` files.

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
| `-s <subset>` | Subset: Define a [GO subset](https://github.com/geneontology/go-ontology/tree/master/src/ontology/subsets) (default: `goslim_agr`) |
| `-i <input>` | Input: Define gene symbols input file (default: `symbols.txt`) |
| `-n` | Names: Retrieve new HGNC ids for symbols.txt file |
| `-r` | Names: Retrieve new ontology data from API |

After the script is run and the IDs are retrieved, the script will process the data and output the groupings into three `.csv` files: `Cellular function (subset).csv`, `Cellular process (subset).csv`, and `Cellular locaiton (subset).csv`.

The script will also output the groupings to the terminal. Here is an example for the `GO:0005576 (extracellular region)` group from the `location` ontology subcategory using the `goslim_agr` GO subset:

```
Ontology grouping type: location

GO:0005576 (extracellular region)
CTRL
SCAMP2
PTBP1
SLC4A1
KLK13
```

## Notes

- The [genenames.org](https://www.genenames.org) API only provides IDs for human genes. As such, if you need IDs for non-human genes, please feel free to rework the part of the script which is used to convert gene symbols into IDs
