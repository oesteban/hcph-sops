

## Executing MRIQC
- [ ] Register the MRIQC container with DataLad containers-run
- [ ] Run MRIQC:
    ```shell
    datalad containers-run \
        --container-name containers/mriqc \
        --input sourcedata \
        --output . \
        '{inputs}' '{outputs}' participant --session lastsession -w workdir
    ```
- [ ] Screen the T1w, DWI and BOLD visual reports, assign a quality assessment using *Q'Kay*
- [ ] If either the dMRI or the RSfMRI quality is insufficient, schedule an extra session after the initially-planned scanning
period to reacquire it.
