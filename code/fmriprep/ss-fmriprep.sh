#!/bin/bash

#SBATCH --partition=russpold
#SBATCH --mem=55GB
#SBATCH --cpus-per-task=4
#SBATCH --time=2-00:00:00
#SBATCH --job-name=fmriprep
#SBATCH --error="slurm-%A_%a.err"

# Submit a Single Session through fMRIPrep

ARGS=($@)
DATADIR=$1
STUDY=`basename $DATADIR`

if [[ -n $SLURM_ARRAY_TASK_ID ]]; then
  SES=${ARGS[`expr ${SLURM_ARRAY_TASK_ID} + 1`]}
else
  SES=$2
fi

echo "Processing: $SES"

IMG="/oak/stanford/groups/russpold/users/cprovins/singularity_images/fmriprep-23.1.4.simg"

WORKDIR="${L_SCRATCH}/fmriprep/${STUDY}/${SES}"
mkdir -p ${WORKDIR}
OUTDIR="${DATADIR}/derivatives2"
mkdir -p $OUTDIR

PATCHES=""

BINDINGS="-B $DATADIR/inputs:/data:ro \
-B ${WORKDIR}:/work \
-B ${OUTDIR}:/out \
-B `pwd`/license.txt:/opt/freesurfer/license.txt \
-B `pwd`/filter_file_$SES.json:/filter_file_$SES.json \
-B ${HOME}/.cache/templateflow/tpl-MNI152NLin6Asym/:${HOME}/.cache/templateflow/tpl-MNI152NLin6Asym/
$PATCHES"

FMRIPREP_CMD="/data /out/fmriprep-23.1.4 participant \
-w /work --bids-filter-file /filter_file_$SES.json --skip_bids_validation \
--fs-subjects-dir /out/fmriprep-23.1.4/sourcedata/freesurfer \
--nprocs 4 --mem 45G --omp-nthreads 2 \
-vv"

#Create json file to filter one session only
echo '{"bold": {"datatype": "func", "session": "'${SES: -2}'", "suffix": "bold"}}' > filter_file_${SES}.json

SING_CMD="singularity run -e $BINDINGS $IMG $FMRIPREP_CMD"
echo $SING_CMD
$SING_CMD
echo "Completed with return code: $?"
