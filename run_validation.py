from owlready2 import get_ontology
from pyshacl import validate
import rdflib
import graphviz
import os


def create_graphviz_file(ontology_path: str):
    onto = get_ontology(ontology_path).load()
    dot = graphviz.Digraph(comment="APT41 Ontology")

    # Add classes
    for cls in onto.classes():
        dot.node(cls.name)

    # Add object properties as edges
    for prop in onto.object_properties():
        for d in prop.domain:
            for r in prop.range:
                dot.edge(d.name, r.name, label=prop.name)

    dot.render("./owl_files/apt41_ontology.gv")


def main():
    # Method 1: Load with explicit format
    owl_file_path = "./owl_files/output_ontology.owl"
    abs_path = os.path.abspath(owl_file_path).replace('\\', '/')

    create_graphviz_file(owl_file_path)

    # Load the ontology with explicit format
    onto = get_ontology(f"file://{abs_path}").load(only_local=True, format="rdfxml")

    # Check loaded classes
    print(list(onto.classes()))

    for prop in onto.object_properties():
        print(f"Object Property: {prop.name}, Domain: {prop.domain}, Range: {prop.range}")

    print("Ontology IRI:", onto.base_iri)
    print("Classes:", len(list(onto.classes())))
    print("Object properties:", len(list(onto.object_properties())))
    print("Data properties:", len(list(onto.data_properties())))
    print("Individuals:", len(list(onto.individuals())))

    data_graph = rdflib.Graph().parse("./output_ontology.owl", format="xml")
    conforms, results_graph, results_text = validate(data_graph, inference='rdfs')
    print(results_text)

if __name__ == "__main__":
    main()