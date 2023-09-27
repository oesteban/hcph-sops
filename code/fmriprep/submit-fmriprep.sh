#!/bin/bash

DATADIR="/oak/stanford/groups/russpold/inprocess/cprovins/hcph-pilot/"
SUB="sub-001"
pushd $DATADIR/inputs/$SUB > /dev/null
ALL_SES=(`ls -d ses-*`)
popd > /dev/null

#Remove session with no fMRI
SES=()
for S in "${ALL_SES[@]}"; do
        if [ -d "$DATADIR/inputs/$SUB/$S/func" ]; then
                SES+=("$S")
        else
            	echo "Session '$S' has no functional scan."
        fi
done

echo "Submitting `basename $DATADIR` with ${#SES[@]} sessions"
# remove one since we are starting at 0
JOBS=`expr ${#SES[@]} - 1`
sbatch --array=0-$JOBS ss-fmriprep.sh $DATADIR ${SES[@]}

