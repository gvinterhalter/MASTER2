-- drop table if EXISTS swissprot;

create table swissprot
(
  id TEXT NOT NULL,
  name TEXT NOT NULL,
  accessions TEXT [] NOT NULL,
  organism TEXT NOT NULL,
  pe TEXT NOT NULL,
  kw TEXT [] NOT NULL,
  go TEXT [][] NOT NULL,
  gomf TEXT [] NOT NULL,
  seq_length INT NOT NULL,
  seq TEXT NOT NULL,

  primary key (id)
);



-- gene ontology


CREATE TABLE IF NOT EXISTS goterms
(
  id          TEXT    NOT NULL,
  is_obsolete BOOLEAN NOT NULL,
  name        TEXT    NOT NULL,
  namespace   TEXT    NOT NULL,
  def         TEXT    NOT NULL,
  comment     TEXT,
  xrefs       TEXT[],
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS go_relations
(
  start_id TEXT NOT NULL,
  end_id   TEXT NOT NULL,
  type     TEXT NOT NULL,
  PRIMARY KEY (start_id, end_id, type),
  FOREIGN KEY (start_id) REFERENCES goterms (id) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (end_id) REFERENCES goterms (id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- keywords

CREATE TABLE IF NOT EXISTS keywords
(
  ac            TEXT NOT NULL,
  name          TEXT NOT NULL,
  category      TEXT,
  category_name TEXT,
  def           TEXT,
  synonyms      TEXT [],
  ww            TEXT [],
  PRIMARY KEY (ac)
);

CREATE TABLE IF NOT EXISTS kw_parent
(
  kw     TEXT NOT NULL,
  parent TEXT NOT NULL,
  PRIMARY KEY (kw, parent),
  FOREIGN KEY (kw) REFERENCES keywords (ac) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (parent) REFERENCES keywords (ac) ON DELETE CASCADE ON UPDATE CASCADE
);


CREATE TABLE IF NOT EXISTS kw2go
(
  kw TEXT NOT NULL,
  go TEXT NOT NULL,
  PRIMARY KEY (kw, go),
  FOREIGN KEY (kw) REFERENCES keywords (ac) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (go) REFERENCES goterms (id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- proteins

CREATE TABLE IF NOT EXISTS valid_proteins
(
  ac            TEXT NOT NULL,
  len           INT  NOT NULL,
  dis40         BOOLEAN,
  dis40_random  BOOLEAN,
  dis40_uniform BOOLEAN,
  dis_smart     BOOLEAN,
  dis_smart_random BOOLEAN,

  PRIMARY KEY (ac)
);

CREATE TABLE IF NOT EXISTS prot2kw
(
  prot TEXT NOT NULL,
  kw   TEXT NOT NULL,
  PRIMARY KEY (kw, prot),
  FOREIGN KEY (kw) REFERENCES keywords (ac) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (prot) REFERENCES valid_proteins (ac) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS prot2go
(
    prot TEXT NOT NULL,
    go TEXT NOT NULL,
    PRIMARY KEY (go, prot),
    FOREIGN KEY (go) REFERENCES goterms (id),
    FOREIGN KEY (prot) REFERENCES valid_proteins (ac)
)