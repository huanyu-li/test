import sys
import os
import itertools
import shutil
import xml.etree.ElementTree
import xml.dom.minidom
from urllib.parse import urlsplit
from collections import defaultdict
from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, XSD
import csv

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

def generate_sssom_tsv_file(mappings_lst, output_file):
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

def rdf2sssom(input_file, output_file, tool):
    mapping_lst = analyze_alignment_in_rdf(input_file, tool)
    print(mapping_lst)
    if len(mapping_lst) > 0:
        generate_sssom_tsv_file(mapping_lst, output_file)

def analyze_alignment_in_rdf(alignment_rdf_file, tool):
    mapping_lst = []
    doc = xml.dom.minidom.parse(alignment_rdf_file)
    o1 = doc.getElementsByTagName('onto1').item(0).firstChild.data
    o2 = doc.getElementsByTagName('onto2').item(0).firstChild.data
    nodes = doc.getElementsByTagName("Cell")
    for node in nodes:
       relation = str(node.getElementsByTagName("relation").item(0).firstChild.data)
       e1 = node.getElementsByTagName("entity1").item(0).getAttribute("rdf:resource")
       e2 = node.getElementsByTagName("entity2").item(0).getAttribute("rdf:resource")
       confidence = node.getElementsByTagName('measure').item(0).firstChild.data
       mapping_lst.append(construct_alignment_output(o1, o2, e1, e2, relation, confidence, tool))
    return mapping_lst 

def main(argv):
    if len(argv) < 4:
        return
    rdf2sssom(argv[1], argv[2], argv[3])

if __name__ == "__main__":
    main(sys.argv)


# python rdf2sssom.py /path/logmap_mappings.rdf ./algnments.tsv LogMap
