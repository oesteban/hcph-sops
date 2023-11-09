## Executing *MRIQC*

- [ ] Create a dataset to host the *MRIQC* derivatives.
    Remember to set the correct version of the container (in our case {{ settings.versions.mriqc }}).
    ``` shell
    cd /data/datasets/hcph-dataset
    datalad create derivatives/mriqc-{{ settings.versions.mriqc }}
    ```
??? warning "We are not yet registering the *MRIQC* derivatives dataset as a sub-dataset."

    To avoid complication at run time, the *MRIQC* derivatives dataset will be added as a sub-dataset to the unprocessed dataset only after *MRIQC* run is completed. As such, note that we are **NOT** using the `-d` flag

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

- [ ] Add the deriatives as a sub-dataset to the unprocessed data.
    ```shell
    cd /data/datasets/hcph-dataset
    datalad create -f -d . derivatives
    ```

- [ ] Push the new derivatives to the remote storage.
    ```shell
    datalad push --to ria-storage
    datalad push --to origin
    ```
- [ ] Screen the T1w, DWI and BOLD visual reports
- [ ] Schedule an extra session after the initially-planned scanning period to reacquire it if either the dMRI or the RSfMRI quality is insufficient.
