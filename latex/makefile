compile:  ref.bib
	latexmk -pdf -jobname=out/master main.tex 

ref.bib: ./bib
	cat ./bib/* > ref.bib
	sed -r "s/url = \{https?:\/\/doi.org\/([^}]+)\}/note = {\\\\href{https:\/\/sci-hub.bz\/\1}{link}}/g" ref.bib > sci.bib


