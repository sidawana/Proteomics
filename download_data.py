from Bio.PDB import PDBList
from Bio.PDB.DSSP import DSSP
from Bio.PDB import MMCIFParser

import pandas as pd
import os
import pickle

import logging


# getting list of proteins
def get_list(protein_list:str)->list:
    """function for returning list of proteins
        :param protein_list: txt file containg pdb-ids seperated by comma(7mdh,8kfp,...)
        :returns : list of all proteins in the file
    """
    with open(protein_list, 'r') as file:
        proteins = file.read().replace('\n', '')
    return proteins.split(',')


def download_proteins(proteins:list,location:str)->None:
    """function to download protein structure files
       :param: proteins:list of proteins
       :param: location: location to store protein structures
    """
    #creating dirs if does'nt exist
    os.makedirs(location, exist_ok=True)
    pdbl = PDBList()

    for protein in proteins:
        pdbl.retrieve_pdb_file(protein, pdir = location,file_format='mmCif')
    print('files have been downloaded')


def parse_proteins_to_dssp(proteins:list,src_location:str,dest_location:str)->list:
    """
    function to parse files to DSSP
    :param:proteins: list of downloaded mmcif proteins
    :param:src_location: location of mmcif protein structure files
    :param:dest_location: destination of dssp file storage
    :returns: dssp_protein_list: list of DSSP converted files 
    """
    parser = MMCIFParser()
    parsed_proteins_list= []
    os.makedirs(dest_location, exist_ok=True)


    for protein in proteins:
        # Extracting structures from the mmcif files
        try:
            protein_structures = parser.get_structure(protein,os.path.join(src_location+protein.lower())+'.cif')
        except Exception as e:
            logging.error('Error while parsing for protein'+protein)
            logging.error('moving to next protein')
            continue
        
        # since there can be many models in the structure of a single protein
        for model in protein_structures:
            try:
                dssp = DSSP(model,os.path.join(src_location+protein.lower())+'.cif', dssp='mkdssp')
                dssp_successful = True
                break # only using the first parsed structure
            except Exception as e:
                logging.error("Error while calculating dihedral angles for model")
                dssp_successful=False
                continue
        
        if dssp_successful:
            # saving dssp structure to a file
            with open(os.path.join(dest_location+protein.lower())+'.pkl', 'wb') as file:
                pickle.dump(dssp, file, pickle.HIGHEST_PROTOCOL)
            parsed_proteins_list.append(protein)

    return parsed_proteins_list


def create_dataframe_from_dssp(dssp_list:list,location:str):
    """function for creating pandas dataframe form Dssp files
        :param:dssp_list: list of dssp parsed proteins
        :param: location: location of Dssp files
        :returns df:dataframe containg all proteins and dihedral angles"""

    df = pd.DataFrame(columns = ['Protein','index_in_protein','Amino_Acid','Secondry_structure',
                             'Phi','Psi','Relative Acessible Surface Area'])

    for protein in dssp_list:
        with open(os.path.join(location+protein.lower())+'.pkl', 'rb') as f:
            dssp = pickle.load(f)
        # each protein contains a lot of residue or amino acids
        for residue in dssp:
            residue = list(residue)
            # replacing NA with None
            residue = [x if x != 'NA' else None for x in residue]
            df = df.append({'Protein': protein,'index_in_protein':residue[0],'Amino_Acid':residue[1]
                    ,'Secondry_structure':residue[2],'Phi':residue[4],'Psi':residue[5],
                    'Relative Acessible Surface Area':residue[3]}, ignore_index=True)
    
    return df