# This script is used for generating other notebook variants for the different conditions
import nbformat as nbf

nb_id = "print/print"
nb = nbf.read(f"{nb_id}.ipynb",as_version=4) #the toy original is the pandas-only control
code = "import lux\nlux.config.lazy_maintain = True"
nb["cells"].insert(0,nbf.v4.new_code_cell(code))
nbf.write(nb, f'{nb_id}_o1.ipynb')

nb = nbf.read(f"{nb_id}.ipynb",as_version=4) 
code = "import lux\nlux.config.lazy_maintain = True\nlux.config.early_pruning = True"
nb["cells"].insert(0,nbf.v4.new_code_cell(code))
nbf.write(nb, f'{nb_id}_o1o2.ipynb')

nb = nbf.read(f"{nb_id}.ipynb",as_version=4) 
code = "import lux\nlux.config.lazy_maintain = True\nlux.config.early_pruning = True\nlux.config.streaming = True"
nb["cells"].insert(0,nbf.v4.new_code_cell(code))
nbf.write(nb, f'{nb_id}_o1o2o3.ipynb')