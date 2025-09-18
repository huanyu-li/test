# Tutorial: Generating Ontology Alignments with LogMap

This tutorial shows how to generate ontology alignments using the [LogMap](https://github.com/ernestojimenezruiz/logmap-matcher) tool.  
LogMap is a state-of-the-art ontology matching system that combines lexical and structural matching strategies and includes logical reasoning to ensure that the resulting ontology network is consistent.

---

## Prerequisites

**Java 11+** (required to run LogMap)  
  Verify with:
  ```bash
  java -version
  ```

## Clone the LogMap repository or download a release
```bash
git clone https://github.com/ernestojimenezruiz/logmap-matcher.git
cd logmap-matcher
```


## compile using maven:
`mvn clean package`

This creates an executable JAR in the `target` directory

Alternatively, download a precompiled distribution from the [relase page](https://github.com/ernestojimenezruiz/logmap-matcher/releases).

## Running LogMap

```bash
java -jar logmap-matcher-<version>.jar MATCHER \
  ontologyA.owl \
  ontologyB.owl \
  ./output/
```

- MATCHER tells LogMap to perform ontology matching.
- ontologyA.owl and ontologyB.owl are the input ontologies.
- ./output/ is the folder where results will be stored.

## Understanding the Output

After running LogMap, the output/ folder will contain:
logmap_mappings.rdf – The alignment in RDF format (recommended for interoperability).
logmap_mappings.txt – The alignment in a simple tabular text format.
logmap_debug.log – Detailed log of the matching process.
A typical mapping in RDF format looks like:

:CEON_Product owl:equivalentClass :DPPO_Product .

## Optional: Converting to SSSOM

For richer metadata, you can convert RDF mappings into the SSSOM tabular format (CSV).
We provide a small converter script in this project:
```bash
python rdf2sssom.py ./output/logmap_mappings.rdf ./output/logmap_mappings.csv
```
