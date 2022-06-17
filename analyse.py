import json
import pathlib
import argparse
import requests
import xmltodict
import csv

parser = argparse.ArgumentParser()
parser.add_argument('-s', help='define search subset', default='goslim_agr')
parser.add_argument('-n', help='retrieve new HGNC ids for symbols.txt file', action='store_true')
parser.add_argument('-r', help='retrieve new ontology data from API', action='store_true')
args = parser.parse_args()

annotations = {'function': {'index': 0, 'dictionary': {}}, 'process': {'index': 1, 'dictionary': {}}, 'location': {'index': 2, 'dictionary': {}}}

my_file = open('symbols.txt', 'r')
geneList = my_file.read().split('\n')
my_file.close()

symbolsFile = 'HGNCids.txt'
if args.n or not pathlib.Path(symbolsFile).is_file():
    symbolSubject = ''
    for symbol in geneList:
        lookupURL = 'https://rest.genenames.org/fetch/symbol/' + symbol
        r = requests.get(lookupURL)
        data = xmltodict.parse(r.content)
        try:
            symbolSubject = symbolSubject + '&subject=' + data['response']['result']['doc']['str'][0]['#text'].replace(':', '%3A')
            print('Retrieved ID for', symbol)
        except NameError:
            print('Error: genenames.org failed to provide an ID for', symbol)

    with open(symbolsFile, 'w') as text_file:
        text_file.write(symbolSubject)
    print('Wrote symbol data to gene_symbols.txt')

else:
    f = open(symbolsFile, 'r')
    symbolSubject = f.read()

subsetDir = args.s + '/'
if args.r or not pathlib.Path(subsetDir).is_dir():
    ontologyURL = 'https://api.geneontology.org/api/ontology/ribbon/?subset=' + args.s + symbolSubject
    r = requests.get(ontologyURL)
    data = r.json()

    for key, value in annotations.items():
        for each in data['categories'][value['index']]['groups']:
            annotations[key]['dictionary'][each['id']] = each['label']

    pathlib.Path(subsetDir).mkdir(parents=True, exist_ok=True)
    for key, value in annotations.items():
        json.dump(annotations[key]['dictionary'], open(subsetDir + key + '_' + args.s + '.txt', 'w'))
        print('Wrote', key, 'data to', subsetDir + key + '_' + args.s + '.txt')

    if len(data['subjects']) != len(geneList):
        print('\nError: Length of retrieved ontology data (' + str(len(data['subjects'])) + ') does not match the number of input genes (' + str(len(geneList)) + '). This means that geneontology.org did not return data for some of the genes.')
        quit()
    geneAttributes = {}
    for index, gene in enumerate(geneList):
        geneAttributes[gene] = []
        for each in data['subjects'][index]['groups']:
            geneAttributes[gene].append(each)

    json.dump(geneAttributes, open(subsetDir + 'ontologies_' + args.s + '.txt', 'w'))
    print('Wrote', key, 'data to', subsetDir + key + '_' + args.s + '.txt')

    print('\nFinished writing ontology data to files')

else:
    geneAttributes = json.load(open(subsetDir + 'ontologies_' + args.s + '.txt'))

    for key, value in annotations.items():
        annotations[key]['dictionary'] = json.load(open(subsetDir + key + '_' + args.s + '.txt'))

skippedTerms = ['other biological process', 'other cellular component']
annotations['location']['dictionary'] = {key: val for key, val in annotations['location']['dictionary'].items() if val not in skippedTerms}

for groupingType in annotations:
    print('\nOntology grouping type:', groupingType)
    writer = csv.writer(open(subsetDir + 'Cellular ' + groupingType + ' (' + args.s + ').csv', 'w'))
    for key, value in annotations[groupingType]['dictionary'].items():
        currentList = [value]
        for gene, array in geneAttributes.items():
            if key in array:
                currentList.append(gene)
        if currentList[1:]:
            print('\n' + key, '(' + value + ')')
            print(*currentList[1:], sep='\n')
            writer.writerow(currentList)

print('\nFinished writing ontology group data')
