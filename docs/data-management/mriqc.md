## Executing *MRIQC*

- [ ] Run *MRIQC*.
    ```shell
    #Assign the variable to the last session ID
    lastsession=01
    datalad containers-run \
        --container-name mriqc \
        --input sourcedata \
        --output ./derivatives/mriqc-23.1.0 \
        "{inputs} {outputs} participant --session-id ${lastsession} -w ${HOME}/tmp/hcph-derivatives/mriqc-23.1.0 --mem 40G"
    ```
- [ ] Push the new derivatives to the remote storage.
    ```shell
    datalad push --to ria-storage
    datalad push --to origin
    ```
- [ ] Screen the T1w, DWI and BOLD visual reports
- [ ] Schedule an extra session after the initially-planned scanning period to reacquire it if either the dMRI or the RSfMRI quality is insufficient.
