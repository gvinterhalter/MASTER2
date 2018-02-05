compile:  ref.bib
	latexmk -pdf -jobname=out/master main.tex 


bib/ref.bib: ref_org.bib
	sed -r "s/url = \{https?:\/\/doi.org\/([^}]+)\}/note = {\\\\href{https:\/\/sci-hub.bz\/\1}{link}}/g" ref_org.bib > ref.bib



