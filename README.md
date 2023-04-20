# Complex_PDB_treating Repository

A repository containing a **terminal launch Python script** to download a selected PDB of a complex (target-ligand) and splitting this PDB file up into two separate files: one for the target and one for the ligand.

The overall command to run the script is:

`splitpdbcomplex.py <PDB code> [optional flags given below]`

Three files appear in the current folder as a result of running the script: the original PDB file `<PDB code>.pdb`, the PDB file `<PDB code>_target.pdb` containing the target PDB formatted coordinates, and the PDB file `<PDB code>_ligand.pdb` containing the ligand PDB formatted coordinates.

## Repository Content

* The main script is called `splitpdbcomplex.py`, situated in the root folder
* Examples can be found in the `/examples` folder.
  * The three aforementioned output PDB files (here 6Y0F as example PDB code)
  * `example_html_code_<PDB code>.txt` is a demonstration of the HTML code that is being used in the example. Read more about how the HTML code matters below. (here 6Y0F as example PDB code)
  * `output_print_example_<PDB code>.txt` is a demonstration of the output that is being printed to the terminal when running the script. (here 6Y0F as example PDB code)
* All other files can be ignored, they are developer specific.

## Script Explained

The `splitpdbcomplex.py` script is explained stepwise. It is important to understand the decisions on which this script is founded to estimate its applicability.

1. Arguments given as input in command line are parsed and stored in variables.
   1. **Obligatory input**
    
        The PDB code is given after the script: `splitpdbcomplex.py <PDB code>`
   2. **Optional flags**

      `-l` or `--ligandcode` - manually specify the ligand code that is used to identify the desired ligand in the PDB file. The default is set to XXX (overwritten at a later stage if this flag is not used).

      `-c` or `--chaincode` - manually specify the chain code that is used to identify the desired chain code(s) of the target (multiple options possible, e.g. `splitpdbcomplex.py <PDB code> -c A B` to select chains A and B). The default is set to A.

      `-lc` or `--ligandchain` - manually specify the chain code that is used to identify the desired chain code(s) of the ligand (multiple options possible, e.g. `splitpdbcomplex.py <PDB code> -lc A B` to select chains A and B). The default is set to A.

2. Read or automatically extract the ligand code. The scenarios are:
   1. A code for the ligand was provided and overwrites the default XXX. Proceed to step 3.
   2. If the ligand code was not specified (still XXX from the default) the following criteria will be checked consecutively:
      1. Check if the PDB website specifies the so-called _Subject of Investigation/LOI_. It does so by checking if one of the following strings are contained a _single time_ within the HTML code: `</a> (Subject of Investigation/LOI)` or `\">(Subject of Investigation/LOI)`. If one of these strings are found, the ligand code is overwritten and the script proceeds to step 3. If two subjects of interest are specified on the website, the script is canceled and a warning tells to check and input manually the ligand code.  
      2. If no subject of interest was found, the script checks whether a so-called _first ligand_ is specified on the website. It does so by searching for the string `var structureFirstLigand =` in the HTML code. When present, the ligand code is extracted from the line containing that string; the script proceeds to step 3. However, the first ligand is not necessarily the actual ligand of interest. Therefore, a warning is displayed if this scenario occurs.
      3. If none of the above strings were found in the HTML code, an error is given (advise to turn to manual mode, using the optional flags) and the program is ended.
   3. IMPORTANT NOTE: all string search above assume only one subject of interest or first ligand. If that is not the case, an error is raised (advise to specify ligand code manually) and the program is ended.
3. Oftentimes there are multiple defined protein/target chains in the PDB file; for instance, in case of multimer protein systems. If the ligand is to sit at the interface of two protein systems, multiple chains should be included. This is brought to the attention of the user through a terminal print after running the code and performing the split in any case. The script counts the amount of times `/sequence/<PDB code>#` occurs. If this is more than one, the warning is raised and you should manually check and potentially rerun the script with additional options.
4. The PDB file is downloaded to the current directory.
5. Create two separate files for the target and ligand.
   1. The target PDB file, `<PDB code>_target.pdb`
      1. The script reads the PDB line per line
      2. If the first four characters of the line are equal to `ATOM` **OR** the first three `TER` **AND** one of the provided chain codes, surrounded by spaces, are contained in that line, the line is copied into the `<PDB code>_target.pdb` file. 
   2. The ligand PDB file, `<PDB code>_ligand.pdb`
         1. The script reads the PDB line per line
         2. If the first six characters of the line are equal to `HETATM` **AND** the line contains the ligand code (extracted or given), separated by two spaces, **AND** the ligand chains are contained within the line, this line is copied into the `<PDB code>_ligand.pdb` file.
6. Some information is printed to the terminal (see `examples/output_print_example_<PDB code>.txt`).


The steps that are undertaken above are based on tested examples. All possible scenarios that we came across are therefore taken into account in the script. 

**However, this does not give any guarantee as to the perfect execution of every single example.**

### Known scenarios the script does not cover
* **6TX6**

