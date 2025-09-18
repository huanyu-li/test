import sys
import os
import itertools
import shutil
import xml.etree.ElementTree
import xml.dom.minidom
from urllib.parse import urlsplit
from collections import defaultdict
# import json

from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, XSD
import csv

default_output_folder =  '/Users/huali50/Downloads/final-mappings/task-a/' 

namespaces = {'xmlns': 'http://example.org/alignment',
              'xmlns:rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
              'xmlns:xsd': 'http://www.w3.org/2001/XMLSchema#'}
sssom_cards = {'=': "https://w3id.org/sssom/MappingCardinalityEnum#1:1"}


def parse_uri(uri):
    parsed_uri = urlsplit(uri)
    if parsed_uri.fragment != '':
        label = parsed_uri.fragment
        base = parsed_uri.scheme + "://" + parsed_uri.netloc + parsed_uri.path
    else:
        label = parsed_uri.path.split('/')[-1]
        base = parsed_uri.scheme + "://" + parsed_uri.netloc + ' '.join(parsed_uri.path.split('/')[0:-1])
    return base, label 

def format_double(value, precision=15):
    return format(value, f'.{precision}f')

def generate_sssom_tsv_file(mappings_lst, onto1_name, onto2_name, tool, output_file):
    if not mappings_lst:
        return # empty list
    header = list(mappings_lst[0].keys())
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=header, delimiter=';')
        writer.writeheader()
        writer.writerows(mappings_lst)
    return

def construct_alignment_output(o1, o2, e1, e2, relation, confidence, tool):
    mapping = defaultdict()
    mapping['subject_id'] = e1
    if len(o1) + len(o2) == 0:
        o1 = parse_uri(e1)[0]
        o2 = parse_uri(e2)[0]
    mapping['subject_source'] = o1
    mapping['object_source'] = o2
    mapping['predicate_id'] = ''
    mapping['object_id'] = e2
    mapping['subject_label'] = parse_uri(e1)[1]
    mapping['object_label'] = parse_uri(e2)[1]
    mapping['confidence'] = confidence
    mapping['tool'] = tool
    mapping['cardinality'] = relation
    mapping['mapping_justification'] = ''
    return mapping

def rdf2sssom(input_file, output_file):
    """
    Example function to convert a file to another format.
    Replace this with your own conversion logic.
    
    :param input_file: Path to the input file
    :param output_format: Desired output file format (e.g., '.txt', '.csv')
    """
    # Example: Open the file and process it based on its type
    # This should be replaced by your actual conversion logic.
    
    base_name = os.path.splitext(input_file)[0].split('/')[-1]  # Remove the old file extension
    print(base_name)
    source_onto_name, target_onto_name, tool = base_name.split('-')[0:3]
        
    mapping_lst = analyze_alignment_in_rdf(input_file, tool)
    print(mapping_lst)
    if len(mapping_lst) > 0:
        generate_sssom_tsv_file(mapping_lst, source_onto_name, target_onto_name, tool, output_file)
        #generate_sssom_ttl_file(mapping_lst, source_onto_name, target_onto_name, tool, default_output_folder + task + '/')

def analyze_alignment_in_rdf(alignment_rdf_file, tool):
    mapping_lst = []
    doc = xml.dom.minidom.parse(alignment_rdf_file)
    print(alignment_rdf_file)
    filename = str(alignment_rdf_file).split('/')[-1].split('.')[0]
    source_onto, target_onto, tool = filename.split('-')
    if tool in ['MATCHA', 'LogMapLt', 'ATM', 'LogMap', 'AMD', 'AML']:
        o1 = source_onto
        o2 = target_onto
    else:
        o1 = doc.getElementsByTagName('onto1').item(0).firstChild.data
        if o1 == 'http://w3id.org CEON ontology full':
            o1 = 'http://w3id.org/CEON/ontology/full'
        o2 = doc.getElementsByTagName('onto2').item(0).firstChild.data
    if tool == 'AMD':
        nodes = doc.getElementsByTagName("cell")
    else:
        nodes = doc.getElementsByTagName("Cell")
    for node in nodes:
       relation = str(node.getElementsByTagName("relation").item(0).firstChild.data)
       e1 = node.getElementsByTagName("entity1").item(0).getAttribute("rdf:resource")
       e2 = node.getElementsByTagName("entity2").item(0).getAttribute("rdf:resource")
       confidence = node.getElementsByTagName('measure').item(0).firstChild.data
       #print(e1, e2, parse_uri(e1), parse_uri(e2), confidence, relation)
       mapping_lst.append(construct_alignment_output(o1, o2, e1, e2, relation, confidence, tool))
    #print(mapping_lst)
    return mapping_lst 
def main(argv):
   if len(argv) < 3:
       return
   process_files_in_folder(argv[1], argv[2])

if __name__ == "__main__":
  main(sys.argv)


 


# python rdf2sssom.py ./output/logmap_mappings.rdf ./output/logmap_mappings.csv
