from download_data import create_dataframe_from_dssp, download_proteins, parse_proteins_to_dssp ,get_list


DSSP_LOCATION = './Data/DSSP/'
PROTEIN_LIST_FILE = "./data/pdb_list.txt"
PDB_LOCATION = './Data/MMCIF/'


if __name__ == "__main__":
    proteins = get_list(PROTEIN_LIST_FILE)
    download_proteins(proteins,PDB_LOCATION)
    dssp_proteins = parse_proteins_to_dssp(proteins,PDB_LOCATION,DSSP_LOCATION)
    data_frame = create_dataframe_from_dssp(dssp_proteins,DSSP_LOCATION)
    data_frame.to_feather('./data/dataset.feather')