#!/bin/bash

endtime=$(date -ud "+3 minutes" +%s)

while [[ $(date -u +%s) -le $endtime ]]
do
    date
    sleep 5
done

