#!/bin/bash

#SBATCH --partition=russpold
#SBATCH --mem=30GB
#SBATCH --cpus-per-task=4
#SBATCH --time=2-00:00:00
#SBATCH --job-name=fmriprep
#SBATCH --error="slurm-%A_%a.err"

# Run only the anatomical workflow of fMRIPrep

DATADIR="/oak/stanford/groups/russpold/inprocess/cprovins/hcph-pilot/"
SUB="sub-pilot"
STUDY=`basename $DATADIR`

echo "Processing the anatomical workflow on subject: $SUB"

IMG="/oak/stanford/groups/russpold/users/cprovins/singularity_images/fmriprep-23.1.4.simg"

WORKDIR="${L_SCRATCH}/fmriprep/${STUDY}/"
mkdir -p ${WORKDIR}
OUTDIR="${DATADIR}/derivatives"
mkdir -p $OUTDIR

PATCHES=""

BINDINGS="-B $DATADIR/inputs:/data:ro \
-B ${WORKDIR}:/work \
-B ${OUTDIR}:/out \
-B `pwd`/license.txt:/opt/freesurfer/license.txt \
-B `pwd`/filter_file_undistorted.json:/filter_file_undistorted.json \
$PATCHES"

FMRIPREP_CMD="/data /out/fmriprep-23.1.4 participant \
-w /work --bids-filter-file ./filter_file_undistorted.json --anat-only --skip_bids_validation \
--nprocs 4 --mem 25G --omp-nthreads 2 \
-vv"

#Create json file to filter undistorted anatomical scans
echo '{"T1w": {"datatype": "anat", "acq": "undistorted", "suffix": "T1w"}}' > filter_file_undistorted.json

SING_CMD="singularity run -e $BINDINGS $IMG $FMRIPREP_CMD"
echo $SING_CMD
$SING_CMD
echo "Completed with return code: $?"
