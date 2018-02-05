import tempfile
import time
import subprocess
import os
import matplotlib
import math


def setFigSize(fig, w, h=None):
    golden_ratio = (1 + 5 ** 0.5) / 2
    h = h or w/golden_ratio
    fig.set_figwidth(w)
    fig.set_figheight(h)


# setup matplotlib options
from matplotlib.backends.backend_pgf import FigureCanvasPgf

matplotlib.backend_bases.register_backend('pdf', FigureCanvasPgf)


def figsize(scale=1):
    #fig_width_pt = 469.755  # Get this from LaTeX using \the\textwidth
    fig_width_pt = 404.02908
    inches_per_pt = 1.0 / 72.27  # Convert pt to inch
    golden_mean = (math.sqrt(5.0) - 1.0) / 2.0  # Aesthetic ratio (you could change this)

    fig_width = fig_width_pt * inches_per_pt * scale  # width in inches
    fig_height = fig_width * golden_mean  # height in inches
    return fig_width, fig_height


pgf_with_latex = {  # setup matplotlib to use latex for output
    "pgf.texsystem": "pdflatex",  # change this if using xetex or lautex
    "text.usetex": True,  # use LaTeX to write all text
    "font.family": "serif",
    "font.serif": [],  # blank entries should cause plots to inherit fonts from the document
    "font.sans-serif": [],
    "font.monospace": [],
    "axes.labelsize": 11,  # LaTeX default is 10pt font.
    "font.size": 11,
    "legend.fontsize": 11,  # Make the legend/label fonts a little smaller
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "figure.figsize": figsize(1),  # default fig size of 0.9 textwidth
    "pgf.preamble": [
        r"\usepackage[utf8x]{inputenc}",  # use utf8 fonts becasue your computer can handle it :)
        r"\usepackage[T1]{fontenc}",  # plots will be generated using this preamble
        r"\usepackage{mathpazo}",  
    ]
}

extra_rcp_options = {
    "savefig.directory": "./plots",
    "axes.grid": True,
    "grid.color": (0.8, 0.8, 0.8),  # grid color
    "grid.linestyle": "dashed",  # dotted
    "grid.linewidth": 0.5,  # in points
}

matplotlib.rcParams.update(pgf_with_latex)
matplotlib.rcParams.update(extra_rcp_options)


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
