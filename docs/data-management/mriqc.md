

## Executing *MRIQC*
!!! info "Just once, the first time you run *MRIQC* on the dataset"
    - [ ] Register the *MRIQC* container to the dataset

        ??? info "Run another version of *MRIQC*"
            In case you want to run another version of *MRIQC*, replace `23.1.0` with the one you intend to use in the command below

        ```
        datalad containers-add --call-fmt 'singularity exec -B {{${HOME}/tmp/}} --cleanenv {img} {cmd}' mriqc --url docker://nipreps/mriqc:23.1.0
        ```
        We configure the containers call to automatically mount the temporary folder, because we will store the working directory there.

- [ ] Run *MRIQC*:
    ```shell
    #Assign the variable to the last session ID
    lastsession=01
    datalad containers-run \
        --container-name mriqc \
        --input sourcedata \
        --output ./derivatives/mriqc-23.1.0 \
        "{inputs} {outputs} participant --session-id ${lastsession} -w ${HOME}/tmp/hcph-dataset/mriqc-23.1.0 --mem 40G"
    ```
- [ ] Push the new derivatives to the remote storage.
    ```shell
    datalad push --to ria-storage
    datalad push --to origin
    ```
- [ ] Screen the T1w, DWI and BOLD visual reports, assign a quality assessment using *Q'Kay*
- [ ] If either the dMRI or the RSfMRI quality is insufficient, schedule an extra session after the initially-planned scanning
period to reacquire it.
