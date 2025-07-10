#!.venv/bin/python

from glob import glob
from ntpath import isfile
from subprocess import call
from os.path import isdir


_PREFIXIES = ["*.aux", 
              "*.fdb_latexmk", 
              "*.fls", 
              "*.log", 
              "*.out", 
              "*.pdf", 
              ".synctex.gz", 
              "*.dvi",
              "*.pgf-plot.gunuplot",
              "*.script", 
              "*.dat",
              "*.toc",
              "*.bbl",
              "*.bcf",
              "*.xml"]


print("WIPING UNWANTED FILES.")

for prefix in _PREFIXIES:
    print(f"{prefix[1:]}...")
    call(["find", ".", "-name", prefix, "-type", "f", "-delete"])


contents = glob("*", recursive=True)
for path in contents:

    splitname = path.split("_")
    qmd_name = "_".join(splitname[:-1])
    qmd_name += ".qmd"
    if splitname[-1] == "files" and isdir(path) and qmd_name in contents:
        call(["rm", "-rf", path])
    


    splitname = path.split(".")
    qmd_name = ".".join(splitname[:-1])
    qmd_name += ".qmd"
    if splitname[-1] in ["tex", "html"] and isfile(path) and qmd_name in contents:
        call(["rm", "-rf", path])

print("COMPLETE!!")
