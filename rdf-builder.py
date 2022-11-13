from __future__ import annotations
import uuid
from typing import Dict

from rdflib import Graph, Literal, URIRef, RDF, FOAF

def _localname(iri: URIRef) -> str:
    return iri[max(iri.rfind("/"), iri.rfind("#")) + 1:]

class RdfGraphBuilder:
    def __init__(self, graph: Graph, namespace: str, seed: any = 0, ns_mapping: Dict[str, str] = {}):
        self.obj_count = 0
        self.graph = graph
        self.namespace = namespace
        self.seed = str(seed)
        [graph.bind(prefix, ns) for prefix, ns in ns_mapping.items()]
    
    def new_object(self, rdf_class: URIRef) -> RdfObjectBuilder:
        obj_hash = uuid.uuid5(uuid.NAMESPACE_URL, self.seed + rdf_class + str(self.obj_count))
        iri = URIRef(self.namespace + _localname(rdf_class).lower() + '_' + str(obj_hash)[-6:])
        self.obj_count = self.obj_count + 1
        self.graph.add((iri, RDF.type, rdf_class))
        return RdfObjectBuilder(self, iri)
        
    def add_to_object(self, iri: URIRef) -> RdfObjectBuilder:
        return RdfObjectBuilder(self, iri)

class RdfObjectBuilder:
    def __init__(self, graph_builder: RdfGraphBuilder, iri: URIRef):
        self.graph = graph_builder.graph
        self.iri = iri
        self.graph_builder = graph_builder
        self.parent_builder = None
    
    def with_object_property(self, rdf_property: URIRef, rdf_class: URIRef) -> RdfObjectBuilder:
        obj_builder = self.graph_builder.new_object(rdf_class)
        obj_builder.parent_builder = self
        self.graph.add((self.iri, rdf_property, obj_builder.iri))
        return obj_builder
    
    def with_literal_property(self, rdf_property: URIRef, value: any) -> RdfObjectBuilder:
        if type(value) is not Literal:
            value = Literal(value)
        self.graph.add((self.iri, rdf_property, value))
        return self
        
    def with_iri_property(self, rdf_property: URIRef, iri: URIRef) -> RdfObjectBuilder:
        self.graph.add((self.iri, rdf_property, iri))
        return self
        
    def end_object_property(self) -> RdfObjectBuilder:
        if self.parent_builder is None:
            return self
        return self.parent_builder
        
    def end_object(self) -> URIRef:
        return self.iri

ns = "http://kibbles#"
ns_mapping = {
    "kbls": ns,
    "foaf": FOAF._NS
}
graph = Graph()
graph_builder = RdfGraphBuilder(graph, ns, seed=0, ns_mapping=ns_mapping)
cat_iri = graph_builder.new_object(FOAF.Person) \
                .with_object_property(FOAF.name, FOAF.name) \
                    .with_literal_property(FOAF.name, 'cat') \
                    .with_literal_property(FOAF.name, 'katto') \
                    .end_object_property() \
                .with_literal_property(FOAF.interest, 'Food') \
                .with_literal_property(FOAF.interest, 'Pigeons') \
                .with_object_property(FOAF.interest, FOAF.Person) \
                    .with_literal_property(FOAF.name, 'Bob') \
                    .with_object_property(FOAF.interest, FOAF.Person) \
                        .with_literal_property(FOAF.name, 'Fred') \
                        .end_object_property() \
                    .end_object_property() \
                    .end_object_property() \
                    .end_object_property() \
                    .end_object_property() \
                .end_object()
                
dog_iri = graph_builder.new_object(FOAF.Person) \
                .with_literal_property(FOAF.name, 'Pupper') \
                .with_iri_property(FOAF.interest, cat_iri) \
                .end_object()
                
graph_builder.add_to_object(cat_iri) \
                .with_iri_property(FOAF.interest, dog_iri)

print(graph.serialize())
