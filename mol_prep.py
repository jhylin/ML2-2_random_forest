## Work-in-progress
## Functions:
# 1) preprocess() - preprocess compounds into RDKit molecules 
# 2) rdkit_2d_descriptors() - generate RDKit 2D descriptors
# 3) feat_imp_plot() - convert feature importance array into a dataframe and bar plot

from rdkit.Chem import Descriptors
import datamol as dm
import pandas as pd
import seaborn as sns


#class preprocess_mol:
    # def __init__(self, row) -> None:
        # self.row = pd.DataFrame
        # ?use self.smiles = smiles
        # then generate mols from smiles might be easier


# disable rdkit messages
dm.disable_rdkit_log()

#  The following function code were adapted with thanks from datamol.io
def preprocess(row):

    """
    Function to preprocess, fix, standardise and sanitise compounds

    :param smiles_column: SMILES column name derived from ChEMBL database from an input dataframe
    :param mol: RDKit molecules
    :return: preprocessed RDKit molecules, standardised SMILES, SELFIES, 
    InChI and InChI keys in the dataframe
    """

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

    # Adding following rows of different molecular representations 
    row["rdkit_mol"] = dm.to_mol(mol)
    row["standard_smiles"] = dm.standardize_smiles(dm.to_smiles(mol))
    row["selfies"] = dm.to_selfies(mol)
    row["inchi"] = dm.to_inchi(mol)
    row["inchikey"] = dm.to_inchikey(mol)
    return row



def rdkit_2d_descriptors(df):
    """
    Function to calculate RDKit 2D descriptors for a list of RDKit molecules

    :param df: an input dataframe containing RDKit molecules
    :param mol: RDKit molecules
    :return: a dataframe containing RDKit 2D descriptors
    """

    # Create a mol list based on RDKit molecules (series object)
    mol_list = df["rdkit_mol"]
    # Convert series object into a list
    mol_list = list(mol_list)

    # Calculate RDKit 2D molecular descriptors
    rdkit_mol_ls = [Descriptors.CalcMolDescriptors(mol) for mol in mol_list]

    # Convert the list of molecules with RDKit 2D descriptors into a dataframe
    df_prep_2d = pd.DataFrame(rdkit_mol_ls)
    #print(df_prep_2d.shape)
    
    return df_prep_2d

    

def feat_imp_plot(feat_imp_array, X_df):

    """
    Function to convert feature importance array into a dataframe, 
    which is then used to plot a bar graph showing feature importance ranking 
    in the random forest (RF) model
    
    :param feat_imp_array: array obtained from feature_importances_ attribute
    or permutation_importance function in scikit-learn

    :param X_df: feature column names from X variable dataframe to be used in the plot

    :return: a barplot showing a feature importances ranking in the RF model
    """

    # Convert the feat_imp array into dataframe
    feat_imp_df = pd.DataFrame(feat_imp_array)

    # Obtain feature names via column names of dataframe
    # Rename the index as "features"
    feature = X_df.columns.rename("features")

    # Convert the index to dataframe
    feature_name_df = feature.to_frame(index = False)

    # Concatenate feature_imp_df & feature_name_df
    feature_df = pd.concat([feat_imp_df, feature_name_df], axis=1)
    # Rename the column for feature importances
    feature_df = feature_df.rename(columns = {0: "feature_importances"})
    # Sort values of feature importances in descending order
    feature_df = feature_df.sort_values("feature_importances", ascending=False)
    
    # Seaborn bar plot
    sns.barplot(
        feature_df, 
        x = "feature_importances", 
        y = "features"
        )