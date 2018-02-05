
# coding: utf-8

# In[2]:

from lark import Lark
from lark import Transformer
import re

from GO.Term import Term

def simple_value(name):
    return lambda self, items: (name, items[0])

class OBOTransformer(Transformer):

    true = lambda self, _: True
    false = lambda self, _: False

    eol = lambda self, _: None

    def id(self, items): return items[0].value  # str
    def class_id(self, items): return items[0]  # str

    def xref_value(self, items): return items[0] # TODO, dodati za strig posle
    xref_no_comma = xref_value
    xref_list = list

    name = lambda self, items: ('name', items[0].value)
    namespace = lambda self, items: ('namespace', items[0].value)
    definition = lambda self, items: ('definition', items[0].value[1:-1], items[1])
    alt_id = simple_value("alt_id")
    xref = simple_value("xref")
    replaced_by = simple_value("replaced_by")
    union_of = simple_value("union_of")
    equivalent_to = simple_value("equivalent_to")
    disjoint_from = simple_value("disjoint_from")
    consider = simple_value("consider")
    subset = simple_value("subset")
    is_obsolete = simple_value("is_obsolete")
    is_anonymous = simple_value("is_anonymous")
    builtin = simple_value("builtin")
    comment = lambda self, items: ('comment', items[0].value)
    created_by = lambda self, items: ('created_by', items[0].value)
    creation_date = lambda self, items: ('creation_date', items[0].value)

    is_a = simple_value("is_a")
    union_of = simple_value("union_of")
    equivalent_to = simple_value("equivalent_to")
    disjoint_from = simple_value("disjoint_from")
    relationship = lambda self, items: ('relationship', items[0].value, items[1])
    synonym = lambda self, items: ('synonym', items[0].value[1:-1], items[1].value, items[2])

    intersection_of = lambda self, items: ("intersection_of", items[0])    #TODO

    def intersection(self, items):
        if len(items) == 1:
            return items[0].value
        else:
            return items[0].value, items[1].value

    property_value= lambda self, items:   None    #TODO

    def term_frame(self, items):
        t = Term(items[0])
        for something in items[2:]:
            clause, eol = something.children
            if clause and type(clause) == tuple:
                tag, v, *vs = clause
                if vs:
                    t.add(tag, (v, *vs))
                else:
                    t.add(tag, v)
        return t

    # start = lambda self, items: items.children
    def start(self, items):
        header, term_frame_list, typedef_list = items
        return term_frame_list.children


# In[3]:

def apply_meta_rules(gramatika):
    gramatika = re.sub(r"([a-z_]+)-TVP",      r' "\1:" UNQUOTED_STRING -> \1',   gramatika)
    gramatika = re.sub(r"([a-z_]+)-BT",       r' "\1:" ( true | false ) -> \1',  gramatika)
    gramatika = re.sub(r"([a-z_]+)-Tag (.*)", r' "\1:" \2 -> \1',                gramatika)
    return gramatika


# In[241]:

parser = Lark(apply_meta_rules(r"""
    start : header? term_frame_list typedef?
    term_frame_list: term_frame+
    header : not_important*
    typedef : "[Typedef]" /(.|\n)+/
    not_important : /.+/? _NL
    
    true: "true"
    false: "false"
       
    class_id : id
    rel_id : id
    instance_id : id
    id : URL_AS_ID | PREFIXED_ID | UNPREFIXED_ID
    URL_AS_ID  : ("https:" | "http:")  /(?:[^\s,\}\]\\\\]|\\\\.)+/
    PREFIXED_ID :  /[^\s:=]+:\s*(?:[^\s,\}\]\\\\]|\\\\.)+/
    UNPREFIXED_ID: /(?:[^\s:,=\}\]\\\\]|\\\\.)+/
 
 
        UNQUOTED_STRING: /.+/

// line termination
    eol :  qualifier_block? HIDDEN_COMMENT? _NL
    HIDDEN_COMMENT : "!" /[^\n]*/
    ?qualifier_block : "{" qualifier_list? "}"
    qualifier_list :  qualifier ("," qualifier)*
    qualifier : rel_id  "="  QUOTED_STRING                 // requiers that ID dosn't allow '='
    
    
    xref_list : "[" (xref_no_comma ("," xref_no_comma)*)? "]"
    xref_value: id QUOTED_STRING?               // instead of 'id' it cold be /\S+/ ???, (does it have to escape ] ?)
    xref_no_comma: id QUOTED_STRING ?
    
        term_frame : "[Term]" _NL "id:" class_id eol something* // (term_frame_clause eol )*
        something : (term_frame_clause eol )

        ?term_frame_clause : is_anonymous-BT
                           | name-TVP
                           | namespace-Tag OBO_NAMESPACE
                           | alt_id-Tag id
                           | "def:" QUOTED_STRING xref_list          -> definition
                           | comment-TVP
                           | subset-Tag id
                           | synonym-Tag QUOTED_STRING SYNONYM_SCOPE NAME? xref_list
                           | xref-Tag xref_value
                           | builtin-BT
                           | property_value-Tag RELATION_ID   /.+/        // TODO
                           | is_a-Tag class_id

                           | intersection_of-Tag    intersection

                           | union_of-Tag class_id
                           | equivalent_to-Tag class_id
                           | disjoint_from-Tag class_id
                           | relationship-Tag RELATION_ID class_id
                           | is_obsolete-BT
                           | replaced_by-Tag class_id
                           | consider-Tag id
                           | created_by-Tag /.+/         -> created_by    // Person-ID
                           | creation_date-Tag /.+/      -> creation_date // ISO-8601-DateTime


        intersection: /[^ !\n]+/
                    | RELATION_ID /[^ !\n]+/

        OBO_NAMESPACE : "cellular_component" | "biological_process" | "molecular_function"
        
        SYNONYM_SCOPE : "EXACT" | "BROAD" | "NARROW" | "RELATED"
        
        RELATION_ID : /[^ !\n]+/
        
        %import common.ESCAPED_STRING -> QUOTED_STRING
        %import common.CNAME -> NAME
        %import common.NEWLINE -> _NL
        %import common.WS_INLINE
        %ignore WS_INLINE


    """), parser="lalr", lexer="contextual",  transformer=OBOTransformer())



# with open("data/go_1.obo", "r") as obo_file:
#     terms = parser.parse(obo_file.read())
#     pass
#
#
# for t in terms:
#     print(t)

