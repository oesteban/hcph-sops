## Within 48h after the FIRST session
!!! danger "Anatomical images must be screened for incidental findings within 48h after the first session"
    
    - [ ] Send the T1-weighted and T2-weighted scan to {{ secrets.people.medical_contact | default("███") }} for screening and incidental findings.
    - [ ] Indicate on [our recruits spreadsheet]({{ secrets.data.recruits_url | default("/redacted.html") }}) that the participant's first session has been submitted for screening.
    - [ ] Wait for response from {{ secrets.people.medical_contact | default("███") }} and note down the result of the screening in our [our recruits spreadsheet]({{ secrets.data.recruits_url | default("/redacted.html") }}).

To do so, you'll need to first [download the data from PACS](#download-the-data-from-the-pacs-with-pacsman-only-authorized-users) and then [convert the data into BIDS](#convert-data-to-bids-with-heudiconv-and-phys2bids) as indicated below.

!!! warning "What to do when there are incidental findings"

    - [ ] Discuss with {{ secrets.people.medical_contact | default("███") }} how to proceed with the participant.
    - [ ] Exclude the participant from the study if {{ secrets.people.medical_contact | default("███") }} evaluates they don't meet the participation (inclusion and exclusion) criteria.

## Within one week after the completed session

### Download the data from the PACS with PACSMAN (only authorized users)

- [ ] Login into the PACSMAN computer  (*{{ secrets.hosts.pacsman }}*)
- [ ] Mount a remote filesystem through sshfs:
    ``` bash
    sshfs {{ secrets.hosts.oesteban | default("<hostname>") }}:/data/datasets/hcph-pilot/sourcedata \
                   $HOME/data/hcph-pilot \
          {{ secrets.data.scp_args | default("<args>") }}
    ```
- [ ] Edit the query file `vim $HOME/queries/last-session.csv` (most likely, just update with the session's date)
``` text title="mydata-onesession.csv"
{% include 'pacsman/mydata-onesession.csv' %}
```
- [ ] Prepare and run PACSMAN, pointing the output to the mounted directory.
    ``` bash
    pacsman --save -q $HOME/queries/last-session.csv \
           --out_directory $HOME/data/hcph-pilot/ \
           --config /opt/PACSMAN/files/config.json
    ```
- [ ] Remove write permissions on the newly downloaded data:
    ``` bash
    chmod -R a-w $HOME/data/hcph-pilot/sub-{{ secrets.ids.pacs_subject | default("01") }}/ses-*
    ```
- [ ] Unmount the remote filesystem:
    ``` bash
    sudo umount $HOME/data/hcph-pilot
    ```

### Retrieve physiological recordings (from {{ secrets.hosts.acqknowledge | default("████") }})

### Copy original DICOMs into the archive of Stockage HOrUs

- [ ] Setup a cron job to execute automatically the synchronization:

    ```
    crontab -e
    [ within your file editor add the following line ]
    0 2 * * * rsync -avurP /data/datasets/hcph-pilot/* {{ secrets.data.curnagl_backup | default("<user>@<host>:<path>") }} &> $HOME/var/log/data-curnagl.log
    ```

## Within two weeks after the completed session

### Convert data to BIDS with HeudiConv

- [ ] Careful to change the number of the session ! Note that we use the heuristic -f reproin, because we have name the sequences at the console following ReproIn convention.
``` bash title="Executing HeudiConv"
{% include 'heudiconv/reproin.sh' %}
```

### Convert physiological recordings and eye-tracking data to BIDS

### Incorporate into version control with DataLad

!!!info "Initiating the version-controled dataset"

    Once at the beginning of the project, the datalad dataset will be created:

    - [ ] Add stockage horus as an SSH remote.


### Run quality control with MRIQC
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
