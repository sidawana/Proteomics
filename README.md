# Proteomics
For the application of <a href= "https://en.wikipedia.org/wiki/Directional_statistics">Directional statistics</a> to protein data we need the <a href="http://guweb2.gonzaga.edu/faculty/cronk/CHEM440pub/dihedral.html">dihedral angles</a>
To extract the data we need to use the <a href ="https://swift.cmbi.umcn.nl/gv/dssp/DSSP_3.html">DSSP</a> algorithm which predicts the dihedral angles in the proteins.

This Run this code build the docker image and run the following command in docker cli
<code> python data_creation.py</code>
after completion of the execution run the following commands in your terminal to copy files from docker to your working directory
<code> docker cp <container id>:/app/data/dataset.feather /your/local/directory</code>
  This command will copy the dataset created to your local directory
