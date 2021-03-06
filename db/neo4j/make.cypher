create index on :GOTerm(id);
create index on :GOTerm(name);
create index on :Keyword(id);
create index on :Keyword(name);

MATCH (k:Keyword)
where k.name in ["Ribonucleoprotein", "Ribosomal protein", "Developmental protein", "Hormone", "Growth factor", "Cytokine", "Neuropeptide", "Activator", "Gap protein", "Repressor", "Chromatin regulator", "Pyrogen", "Vasoactive", "Amphibian defense peptide", "GTPase activation", "Endorphin", "Opioid peptide", "Protein phosphatase inhibitor", "Cyclin"]
set k :mf20dis;

MATCH (k2:Keyword)
where k2.name in ["Oxidoreductase", "Transferase ", "Lyase", "Hydrolase ", "Isomerase", "Glycosidase", "Glycosyltransferase", "Acyltransferase", "Methyltransferase", "Kinase", "Ligase", "Decarboxylase", "Monooxygenase", "Metalloprotease", "Aminopeptidase", "Dioxygenase", "Aminoacyl-tRNA synthetase", "Protease", "Aminotransferase"]
set k2 :mf20ord;