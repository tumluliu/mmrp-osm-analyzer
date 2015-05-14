#!/bin/bash

CSV_DIR=$1
DEST_CSV_FILE=$2
FILE_INDEX=1

FILE_COUNT=$(ls -l $CSV_DIR/*.csv | grep -v ^l | wc -l)
echo "Concatenating CSV files... "
for csv_f in "$CSV_DIR"/*.csv
do
    echo -ne "$FILE_INDEX / $FILE_COUNT\r\c"
    if [ $FILE_INDEX == 1 ]
    then
        cat "$csv_f" > "$DEST_CSV_FILE"
    else
        tail -n +2 "$csv_f" >> "$DEST_CSV_FILE"
    fi
    let "FILE_INDEX+=1"
done
echo "done!"

