## Executing fMRIPrep
In order to run multiple sessions in parallel for a single subject, a trick needs to be applied to avoid several jobs to work simultaneously on the same file thus compromising it.

- [ ] First, run only the anatomical workflow through a single fMRIPrep instance to fetch the needed template from templateflow and to generate the outputs of FreeSurfer. 
``` bash title="Executing anatomical workflow of fMRIPrep"
{% include 'code/fmriprep/ss-fmriprep-anatonly.sh' %}
```

- [ ] Once that process is successfull, you can run the sessions in parallel using the `--bids-filter-file` to launch one session per job and the `--fs-subjects-dir` flag to inform the process that the anatomical derivatives already exist.
``` bash title="Launch each session through fMRIPrep in parallel"
cd code/fmriprep
bash submit-fmriprep.sh
```