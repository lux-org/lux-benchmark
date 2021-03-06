# This script is used for generating other notebook variants for the different conditions
import nbformat as nbf

nb_id = "communities/communities"
nb = nbf.read(f"{nb_id}.ipynb",as_version=4) #the toy original is the pandas-only control
code = "import lux"
nb["cells"].insert(0,nbf.v4.new_code_cell(code))

# Explicit compute_meta_recs at every non-print cell
i=0
for cell in nb["cells"]:
    if i>2:
        if ("# {{NO LUX}}"in cell["source"] and "df" in cell["source"]):
            cell["source"] = cell["source"]+"\ndf.compute_meta_recs()"        
    i+=1

nbf.write(nb, f'{nb_id}_baseline.ipynb')

nb = nbf.read(f"{nb_id}.ipynb",as_version=4) 
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