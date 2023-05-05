## Within one week after the completed session

### Download the data from the PACS with PACSMAN (only authorized users)

- [ ] Login into the PACSMAN computer  (*{{ secrets.hosts.pacsman }}*)
- [ ] Mount a remote filesystem through sshfs:
    ``` bash
    sshfs {{ secrets.hosts.oesteban }}:/data/datasets/hcph-pilot/rawdata \
                   $HOME/data/hcph-pilot \
          {{ secrets.data.scp_args }}
    ```
- [ ] Edit the query file `vim $HOME/queries/mydata-onesession.csv` (most likely, just update with the session's date)
``` text title="mydata-onesession.csv"
{% include 'pacsman/mydata-onesession.csv' %}
```
- [ ] Prepare and run PACSMAN, pointing the output to the mounted directory.
    ``` bash
    conda activate pacsman_min_dev_v2
    python /home/localadmin/Bureau/PACSMAN/PACSMAN/pacsman.py --save \
           -q $HOME/queries/mydata-onesession.csv \
           --out_directory $HOME/data/hcph-pilot/ \
           --config /home/localadmin/Bureau/PACSMAN/PACSMAN/files/config_RESEARCH.json
    ```
- [ ] Remove write permissions on the newly downloaded data:
    ``` bash
    chmod -R a-w $HOME/data/hcph-pilot/sub-{{ secrets.ids.pacs_subject }}/ses-*
    ```
- [ ] Unmount the remote filesystem:
    ``` bash
    sudo umount $HOME/data/hcph-pilot
    ```

### CRITICAL: <span style="color: red">WITHIN 48h after the FIRST session</span>

- [ ] Send the T1-weighted and T2-weighted scan to {{ secrets.people.medical_contact }} for screening and incidental findings.

### Retrieve physiological recordings (from {{ secrets.hosts.acqknowledge }})

### Copy original DICOMs into the archive of Stockage HOrUs


## Within two weeks after the completed session

### Convert data to BIDS with HeudiConv and Phys2BIDS

- [ ] Careful to change the number of the session ! Note that we use the heuristic -f reproin, because we have name the sequences at the console following ReproIn convention.
``` bash title="Executing HeudiConv"
{% include 'heudiconv/reproin.sh' %}
```

### Incorporate into version control with DataLad
