BPFind v. 1.8
(http://www.saha.ac.in/biop/dhananjay.bhattacharyya/bpfind.tar.gz)

Please cite the reference while using BPFind tool:

Non-canonical Base Pairs and Higher Order Structures in Nucleic Acids: Crystal 
Structure Database Analysis(2006), 
Das, J.; Mukherjee, S.; Mitra, A.; Bhattacharyya, D., J. Biomol. Struct. Dynam.,
24,149.


(For any query, please mail to: dhananjay.bhattacharyya@saha.ac.in)


BPFind is a software tool for detecting stable and feasible basepairs present in
nucleic acid molecules. It finds potential H-bonds within the molecule and 
checks for the basepair geometry to output the best possible pairing pattern 
between a pair of bases. BPFind considers both the standard N/O-H...N/O and
non-polar C-H...O/N types of hydrogen bonding.  However, one can also detect
those basepairs stabilized only by regular polar hydrogen bonds.


1. Input File Type:
-------------------

Files containing coordinates of the atoms in PDB format (XXXX.pdb). 

2. Output File Description:
---------------------------

XXXX.cor - Contains coordinates of the nucleic acids only considered for 
           searching H-bonds. Base moieties, not having all the 
           purine/pyrimidine ring atoms and C1' atoms, are not considered for 
           basepairing. Therefore, they are not included in XXXX.cor files.
XXXX.out - Contains detailed descriptions of the basepairing patterns present 
           within the RNA molecule.Format is as below:
XXXX.nup - Contains basepairing information required to run the associated
           basepair parameter calculation program NUPARM.  The NUPARM software
           can also be downloaded from the same site.
XXXX.dat - Contains base pairing information of each nucleotide residue in 
           symple format, such as H for Watson-Crick basepairs, N for non-
	   canonical basepairs, T for base triples and L for nonpaired bases
XXXX.hlx - Contains base pairing information of only the double helices, 
           ignoring the unpaired as well as isolated pairs.

The XXXX.out file gives the basepairing informations in the following way:
================================================================================
Column starting from '>' mark represent the following:
>Serial number of nucleotides
----->Residue number as in PDB
---------->Residue name
--------------->Chain ID
---------------->Serial number of the paired base
--------------------->Residue number of the paired base as in PDB
-------------------------->Residue name of the paired base
------------------------------->Chain ID of the paired base
--------------------------------->Base pair type
-------------------------------------->Base pair indicator
--------------------------------------->E-value indicating base pair deformation
------------------------------------------->Equivalent info for other pairs
================================================================================

XXXX.fasta - Contains sequence of the nucleotide chains in a PDB file with 
             residues having coordinates of all ring atoms and C1' atom.

XXXX.hlx - Contains the pseudo-continuous stack regions in the nucleic acid
           molecule as given by their BPFind numbering.



3. Abbreviations Used in Output Files:
--------------------------------------

W - Watson-Crick edge
H - Hoogsteen edge
S - Sugar edge
w - Watson-Crick edge with one or more C-H...O/N type of hydrogen bond
h - Hoogsteen edge with one or more C-H...O/N type of hydrogen bond
s - Sugar edge with one or more C-H...O/N type of hydrogen bond
+ - Protonated Watson-Crick edge
z - Protonated Sugar edge
C - Cis
T - Trans


4. Runtime Options:
-------------------

USAGE: BPFIND -[options] filename

The following options can be used:
-HD [value] to set default hydrogen bond distance cutoff (default = 3.8)
-VA [value] to set default pseudo angle cutoff (default = 120.0)
-EN [value] to set default E-value cutoff (default = 1.8)
-HT to include HETATM entries in PDB
-CH to avoid identification of base pairs stabilized by C-H...O/N H-bonds
-SG to avoid identification of base pairs involving sugar O2' atoms
-AB to avoid base pairing between residue no. i and i+1
-OL to avoid printing base pairing information w.r.t.the second strand.  
 This is suitable for simple oligonucleotides
-ML [character] to detect base pairing within a particular selected chain of DNA/RNA
-NMR to calculate base pairing information for the first model in NMR derived
ensemble of structures

5. Basepairing Criteria:
------------------------

BPFind maintains a few criteria for detecting basepairs:

(i)   Bases not having coordinates of all the ring atoms (purine/pyrimidine) and
      C1' atoms are not considered for detecting hydrogen bonds.
(ii)  At least two hydrogen bonds must exist between two bases, at least one of
      which must be between the base moieties. Basepairs involving both 2'-OH 
      mediated hydrogen bonds are not detected by BPFind. It considers basepairs
      for which both the H-bonds are of C-H...O/N type, as long as one H-bond is
      found between the base rings.
(iii) BPFind considers a range of modified bases which are usually under the 
      'HETATM' lines in a PDB file. They are listed in the four files:
      AdeVariants.name 
      Guavariants.name
      CytVariants.name
      UraVariants.name
      We keep these files in /usr/local/bin directory and the program also
      expects them there.  In case you want to keep them somewhere else,
      please modify the code (line nos. 57, 65, 73 and 81) to indicate the
      location of these files.
      Any new modified residue name can be included in one of these files 
      accordingly in order to be recognized by  BPFind.
(iv)  BPFind uses a cutoff distance of 3.8 angstrom between the acceptor and 
      donor atoms, a cutoff angle of 120.0 degree for checking planarity of 
      precursor atoms (designed carefully to accommodate more labile basepairs) 
      and a cutoff E-value of 1.8 to signify the overall distortion and maintain
      a good basepairing geometry.
(v)   BPFind uses a more stringent option for protonated basepair options in 
      order to avoid false positives. It considers cutoff angle of 150.0 degree
      for protonated basepairs.
(vi)  BPFind allows more flexibility if 2'-OH of the ribose sugar moiety is 
      involved in hydrogen bonding - a cutoff angle of 100.0 degree.
