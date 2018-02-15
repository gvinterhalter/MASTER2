import tempfile
import time
import subprocess
import os


##-----------------------------------------##
## Compile and show Dataframe as pdf/latex ##
##-----------------------------------------##


def show_latex_table(source):
    with tempfile.NamedTemporaryFile("w", suffix='.tex') as f:
        source = source.replace('{tabular}', '{longtable}')
        source = source.replace('{tabular}', '{longtable}')
        f.write(
            r"""
            \documentclass{article}
            \usepackage{booktabs}
            \usepackage{longtable}
            \begin{document}
            \begin{center}
            %s
            \end{center}
            \end{document}
            """ % source)
        f.flush()
        name = '__latex_tmp'
        r = subprocess.run(['latexmk', f'-jobname={name}', '-pdf', f.name])

    if r.returncode == 0:
        subprocess.Popen(["xdg-open", name + '.pdf'])
        time.sleep(1)
    else:
        print(r)

    for fname in os.listdir("."):
        if fname.startswith(name):
            os.unlink(fname)

    return
