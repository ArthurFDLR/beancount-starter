#!/bin/bash

bean-identify ../ledger-importers.py ../import-statements

while true; do
    read -p "Proceed? [y/n]" yn
    case $yn in
        [Yy]* ) bean-extract ../ledger-importers.py ../import-statements > ../ingestion_result.bean && bean-file -o ../documents ../ledger-importers.py ../import-statements; break;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
done
