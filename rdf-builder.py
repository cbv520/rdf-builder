from __future__ import annotations
import uuid

class RdfGraphBuilder:
    def __init__(self):
        pass
    
    def new_object(self, rdf_class: str) -> RdfObjectBuilder:
        return RdfObjectBuilder(self, rdf_class)

class RdfObjectBuilder:
    def __init__(self, graph_builder: RdfGraphBuilder, rdf_class: str):
        self.id = rdf_class + '_' + str(uuid.uuid4())[-6:]
        self.graph_builder = graph_builder
        self.rdf_class = rdf_class
        print(f'{self.id} a {rdf_class}')
    
    def with_object_property(self, rdf_property: str, rdf_class: str) -> RdfObjectBuilder:
        obj = self.graph_builder.new_object(rdf_class)
        obj.parent = self
        print(f'{self.id} {rdf_property} {obj.id}') 
        return obj
    
    def with_literal_property(self, rdf_property: str, value: any) -> RdfObjectBuilder:
        print(f'{self.id} {rdf_property} {value}')
        return self
        
    def with_iri_property(self, rdf_property: str, iri: str) -> RdfObjectBuilder:
        print(f'{self.id} {rdf_property} {iri}')
        return self
        
    def end_object_property(self) -> RdfObjectBuilder:
        return self.parent
        
    def end_object(self) -> str:
        return self.id
        
graph_builder = RdfGraphBuilder()
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
                .end_object()
                
graph_builder.new_object('Dog') \
                .with_literal_property('hasName', 'Pupper') \
                .with_iri_property('friendsWith', cat_iri) \
                .end_object()

