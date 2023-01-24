
### Data management

#### Within one week from the completed session

- [ ] Download the data from the PACS with PACSMAN (only authorized users)
    - [ ] Login into the PACSMAN computer  (`hos54889`)
    - [ ] Mount a remote filesystem through sshfs:
          ```
          sshfs hos65851:/data/datasets/hcph-pilot/rawdata /home/oesteban/data/hcph-pilot -p 3389 -o idmap=user,gid=100
          ```
    - [ ] Edit a query file (most likely, update with the session's date
    - [ ]  Prepare and run PACSMAN, pointing the output to the mounted directory.
          ```
          conda activate
          python /home/localadmin/Bureau/PACSMAN/PACSMAN/pacsman.py --save -q ~/queries/mydata-onesession.csv --out_directory /home/oesteban/data/hcph-pilot/ --config /home/localadmin/Bureau/PACSMAN/PACSMAN/files/config_RESEARCH.json
          ```
    - [ ] Remove write permissions on the newly downloaded data:
          ```
          chmod -R a-w rawdata/sub-2022_11_07_15_37_06_STD_1_3_12_2_1107_5_99_3/ses-*
          ```
- [ ] Convert data to BIDS with HeudiConv [will change when we adopt reproin]
    ```
    heudiconv -s "pilot" -ss "08" -f ~/tmp/heuristic.py -b -o . --files rawdata/sub-2022_11_07_15_37_06_STD_1_3_12_2_1107_5_99_3/ses-20230116131825/
    ```