## Within one week from the completed session

- [ ] **Download the data from the PACS with PACSMAN** (only authorized users)
    - [ ] Login into the PACSMAN computer  (`hos54889`)
    - [ ] Mount a remote filesystem through sshfs:
        ``` bash
        sshfs hos65851:/data/datasets/hcph-pilot/rawdata \
                       $HOME/data/hcph-pilot \
              -p 3389 -o idmap=user,gid=100
        ```
    - [ ] Edit the query file `vim $HOME/queries/mydata-onesession.csv` (most likely, just update with the session's date)
``` text title="mydata-onesession.csv"
{% include 'pacsman/mydata-onesession.csv' %}
```
    - [ ] Prepare and run PACSMAN, pointing the output to the mounted directory.
        ``` bash
        conda activate
        python /home/localadmin/Bureau/PACSMAN/PACSMAN/pacsman.py --save \
               -q $HOME/queries/mydata-onesession.csv \
               --out_directory $HOME/data/hcph-pilot/ \
               --config /home/localadmin/Bureau/PACSMAN/PACSMAN/files/config_RESEARCH.json
        ```
    - [ ] Remove write permissions on the newly downloaded data:
        ``` bash
        chmod -R a-w $HOME/data/hcph-pilot/rawdata/\
                     sub-2022_11_07_15_37_06_STD_1_3_12_2_1107_5_99_3/ses-*
        ```
    - [ ] Unmount the remote filesystem:
        ``` bash
        sudo umount $HOME/data/hcph-pilot
        ```
- [ ] **Copy original DICOMs into the archive of Stockage HOrUs**.
- [ ] **Convert data to BIDS with HeudiConv and Phys2BIDS**.
    - [ ] Careful to change the number of the session ! Note that we use the heuristic -f reproin, because we have name the sequences at the console following ReproIn convention.
``` bash title="Executing HeudiConv"
{% include 'heudiconv/reproin.sh' %}
```
- [ ] **Incorporate into version control with DataLad**
