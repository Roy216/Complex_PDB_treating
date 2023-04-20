#!/usr/bin/env python
# CHANGE HEADER TO THE SPECIFICS OF YOUR OWN SYSTEM

# Import modules and packages
import urllib.request
import argparse
import requests
import os

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("pdbcode", help="PDB code of system to be downloaded and treated")
parser.add_argument('-l', '--ligandcode', default="XXX",
                    help="Code of the ligand within the PDB file, catches this from the website if not specified")
parser.add_argument('-c', '--chain', nargs='+', default="A",
                    help="Add the chain of the protein to be added to the final file, takes only 'A' if not specified")
parser.add_argument('-lc', '--ligandchain', nargs='+', default="A",
                    help="Specify the ligand chain(s) to consider, takes only 'A' if not specified")
args = parser.parse_args()

# Store input arguments
pdb = args.pdbcode
ligandcode = args.ligandcode
chaincodes = args.chain
ligchaincode = args.ligandchain

page = requests.get('https://www.rcsb.org/structure/' + pdb)
f = open("page.txt", "w", encoding="utf-8")
f.write(str(page.text))
f.close()

# Capture the ligand code from the PDB webpage if no code is given by the user
#
# First check: subject of interest strings present in HTML?
if ligandcode == "XXX":
    with open("page.txt", encoding="utf-8") as file:
        for item in file:
            if "</a> (Subject of Investigation/LOI)" in item:
                if item.count("</a> (Subject of Investigation/LOI)") == 1:
                    idx1 = item.index("</a> (Subject of Investigation/LOI)")
                    ligandcode = str(item[idx1 - 3:idx1])
                else:
                    print(" ")
                    print(
                        "[" + pdb + "] WARNING: Multiple \"Subjects of Interest\" found. This programme can handle only one. Please rerun and specify the ligandcode with the -l flag.")
                    print("Programme has been stopped.")
                    print(" ")
                    os.remove("page.txt")
                    exit()
            elif "\">(Subject of Investigation/LOI)" in item:
                if item.count("\">(Subject of Investigation/LOI)") == 1:
                    idx1 = item.index("\">(Subject of Investigation/LOI)")
                    ligandcode = str(item[idx1 - 3:idx1])
                else:
                    print(" ")
                    print(
                        "[" + pdb + "] WARNING: Multiple \"Subjects of Interest\" found. This programme can handle only one. Please rerun and specify the ligandcode with the -l flag.")
                    print("Programme has been stopped.")
                    print(" ")
                    os.remove("page.txt")
                    exit()

# Second check: see if any first ligand present if no ligandcode was found during first check.
if ligandcode == "XXX":

    with open("page.txt", encoding="utf-8") as file:
        for item in file:
            if "var structureFirstLigand =" in item:
                ligandcode = item[item.find(' "') + len(' "'):item.rfind('";')]
                print(" ")
                print(
                    "[" + pdb + "] WARNING: No \"Subjects of Interest\" found to find the ligand code. Instead, the first specified ligand has been considered the correct one. Please check if this is correct or rerun the programme with a manual input of the ligand code using the -l flag.")

# Third check: if the ligandcode is still not overwritten, return an error.
if ligandcode == "XXX":
    print(" ")
    print("[" + pdb + "] WARNING: No known strings were found in the HTML code, necessary to capture the ligand code.")
    print("Programme has been stopped.")
    print(" ")
    os.remove("page.txt")
    exit()

# Check if the protein is a monomer or not (potentially needing to specify multiple chains)
monomer = "YES"
with open("page.txt", encoding="utf-8") as file:
    for item in file:
        if item.count("/sequence/" + pdb + "#") != 1:
            monomer = "NO"

os.remove("page.txt")

# Fetch the PDB file online
# print("PDB code that will be treated: " + pdb)
url_pdb = 'http://files.rcsb.org/download/' + pdb + '.pdb'
inputfile = pdb + '.pdb'
urllib.request.urlretrieve(url_pdb, inputfile)

# Execute split of target and ligand in separate PDB files
#
# TARGET
proteinline = []
chainstrs = [" " + e + " " for e in chaincodes]
with open(inputfile) as f:
    for line in f:
        if ((line[0:4] == "ATOM") or (line[0:3] == "TER")) and any(chain in line for chain in chainstrs):
            proteinline.append(line)

f = open(pdb + "_target" + ".pdb", "w")
f.close()
for item in proteinline:
    f = open(pdb + "_target" + ".pdb", 'a')
    f.write(item)

# LIGAND
ligandline = []
ligandcodestring = " " + ligandcode + " "
testotherligand = "A" + ligandcode + ""
ligchainstrs = [" " + e + " " for e in ligchaincode]
mult_lig = "NO"
with open(inputfile) as f:
    for line in f:
        if ((line[0:6] == "HETATM") and (ligandcodestring in line)) and any(chain in line for chain in ligchainstrs):
            ligandline.append(line)
        elif ((line[0:6] == "HETATM") and (testotherligand in line)) and any(chain in line for chain in ligchainstrs):
            mult_lig = "YES"

f = open(pdb + "_ligand" + ".pdb", "w")
f.close()
for item in ligandline:
    f = open(pdb + "_ligand" + ".pdb", 'a')
    f.write(item)

# Print information in the terminal
if mult_lig == "YES":
    print(" ")
    print("splitcomplex.py script information")
    print("==================================")
    print("     PDB code: " + str(pdb))
    print("     Chain(s): " + str(chaincodes))
    print("     Ligand code: " + str(ligandcode))
    print("     Ligand chain(s): " + str(ligchaincode))
    print(" ")
    print(
        "     [" + pdb + "] WARNING: multiple ligands of the same kind but in different poses/positions identified! Do a manual check!")
    print(" ")
    print("==================================")
else:
    print(" ")
    print("splitcomplex.py script information")
    print("==================================")
    print("     PDB code: " + str(pdb))
    print("     Chain(s): " + str(chaincodes))
    print("     Ligand code: " + str(ligandcode))
    print("     Ligand chain(s): " + str(ligchaincode))
    print(" ")
    print("     [" + pdb + "] SUCCES")
    print(" ")
    print("==================================")

if monomer == "YES":
    print(" ")
else:
    print(
        "[" + pdb + "] WARNING: the PDB file contains multiple target chains, indicative of multimers. please check if the correct protein chains are included.")
    print(" ")
