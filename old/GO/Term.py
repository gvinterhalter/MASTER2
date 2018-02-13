

class Term:

    def default(self):
        return self.__dict__

    def add(self, name, value):
        if type(getattr(self, name)) == list:
            getattr(self, name).append(value)
        else:
            setattr(self, name, value)

    def __init__(self, manual_id, d=None):
        if d: # imamo dict sa vrednostima
            if '_id' in d: # ako importujemo iz mongo db-a
                del d['_id']
            self.__dict__.update(d)
            return

        self.id = manual_id

        self.name  = None
        self.namespace = None
        self.alt_id = []
        self.definition = None
        self.comment = None
        self.subset = []
        self.synonym = []
        self.xref = []
        self.builtin = False
        self.property_value = []
        self.is_a = []
        self.intersection_of = []
        self.union_of = []
        self.equivalent_to = []
        self.disjoint_from = []
        self.relationship = []
        self.is_obsolete = False
        self.replaced_by = None
        self.consider = []
        self.created_by = None
        self.creation_date = None

    def namespace_short(self):
        return (self.namespace == "biological_process" and "BP" or
                self.namespace == "molecular_function" and "MF" or "CC")

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        s = self
        return f"""\
Term(
    id={s.id},
    name={s.name},
    namespace={s.namespace},
    def={s.definition},
    is_a={s.is_a}
)\
"""

