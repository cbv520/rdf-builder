from __future__ import annotations
import uuid

class RdfGraphBuilder:
    def __init__(self, namespace: str, seed: any = 0):
        self.obj_count = 0
        self.namespace = namespace
        self.seed = str(seed)
    
    def new_object(self, rdf_class: str) -> RdfObjectBuilder:
        obj_hash = uuid.uuid5(uuid.NAMESPACE_URL, self.seed + rdf_class + str(self.obj_count))
        iri = self.namespace + rdf_class.lower() + '_' + str(obj_hash)[-6:]
        self.obj_count = self.obj_count + 1
        print(f'{iri} a {rdf_class}')
        return RdfObjectBuilder(self, iri)
        
    def add_to_object(self, iri: str) -> RdfObjectBuilder:
        return RdfObjectBuilder(self, iri)

class RdfObjectBuilder:
    def __init__(self, graph_builder: RdfGraphBuilder, iri: str):
        self.iri = iri
        self.graph_builder = graph_builder
        self.parent_builder = None
    
    def with_object_property(self, rdf_property: str, rdf_class: str) -> RdfObjectBuilder:
        obj_builder = self.graph_builder.new_object(rdf_class)
        obj_builder.parent_builder = self
        print(f'{self.iri} {rdf_property} {obj_builder.iri}') 
        return obj_builder
    
    def with_literal_property(self, rdf_property: str, value: any) -> RdfObjectBuilder:
        print(f'{self.iri} {rdf_property} Literal({value})')
        return self
        
    def with_iri_property(self, rdf_property: str, iri: str) -> RdfObjectBuilder:
        print(f'{self.iri} {rdf_property} {iri}')
        return self
        
    def end_object_property(self) -> RdfObjectBuilder:
        if self.parent_builder is None:
            return self
        return self.parent_builder
        
    def end_object(self) -> str:
        return self.iri
        
graph_builder = RdfGraphBuilder("http://kibbles#")
graph_builder = RdfGraphBuilder("")
cat_iri = graph_builder.new_object('Cat') \
                .with_object_property('hasName', 'Name') \
                    .with_literal_property('en', 'cat') \
                    .with_literal_property('jp', 'katto') \
                    .end_object_property() \
                .with_literal_property('likes', 'Food') \
                .with_literal_property('hates', 'Pigeons') \
                .with_object_property('owner', 'Person') \
                    .with_literal_property('hasName', 'Bob') \
                    .with_object_property('friendsWith', 'Person') \
                        .with_literal_property('hasName', 'Fred') \
                        .end_object_property() \
                    .end_object_property() \
                    .end_object_property() \
                    .end_object_property() \
                    .end_object_property() \
                .end_object()
                
dog_iri = graph_builder.new_object('Dog') \
                .with_literal_property('hasName', 'Pupper') \
                .with_iri_property('loves', cat_iri) \
                .end_object()
                
graph_builder.add_to_object(cat_iri) \
                .with_iri_property('hates', dog_iri)
