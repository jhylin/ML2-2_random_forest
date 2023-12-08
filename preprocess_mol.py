## Work-in-progress
## Combine preprocessing compounds into RDKit molecules 
## and generate RDKit 2D descriptors

import datamol as dm
import pandas as pd


class preprocess_mol:

    def __init__(self, row) -> None:
        # ?use self.smiles = smiles
        # then generate mols from smiles might be easier
        self.row = pd.DataFrame


    # list_of_mol = df["smiles_col"] #creates a Series object
    # list_of_mol = list(list_of_mol) # converts Series into a List object

    # disable rdkit messages
    dm.disable_rdkit_log()

    # preprocess function to sanitise compounds - adapted from datamol.io
    def preprocess_mol(self, row):
        # smiles_column = strings object
        smiles_column = "canonical_smiles"
        # Convert each compound into a RDKit molecule in the smiles column
        mol = dm.to_mol(row[smiles_column], ordered=True)
        # Fix common errors in the molecules
        mol = dm.fix_mol(mol)
        # Sanitise the molecules 
        mol = dm.sanitize_mol(mol, sanifix=True, charge_neutral=False)
        # Standardise the molecules
        mol = dm.standardize_mol(
            mol,
            # Switch on to disconnect metal ions
            disconnect_metals=True,
            normalize=True,
            reionize=True,
            # Switch on "uncharge" to neutralise charges
            uncharge=True,
            # Taking care of stereochemistries of compounds
            stereo=True,
        )

        row["rdkit_mol"] = dm.to_mol(mol)
        row["standard_smiles"] = dm.standardize_smiles(dm.to_smiles(mol))
        #row["selfies"] = dm.to_selfies(mol)
        #row["inchi"] = dm.to_inchi(mol)
        #row["inchikey"] = dm.to_inchikey(mol)
        return row
    

    

