#!/bin/bash

# Create temporary directory and files
TEMP_DIR=$(mktemp -d)
mkdir "$TEMP_DIR/dir1"
touch "$TEMP_DIR/dir1/test1.py"
touch "$TEMP_DIR/dir1/test2.txt"
mkdir "$TEMP_DIR/dir2"
touch "$TEMP_DIR/dir2/test3.py"
touch "$TEMP_DIR/dir2/test4.txt"

# Run the main program
python -m repopg --dir "$TEMP_DIR" --ext ".py" > output.txt

# Check if the output includes .py files
grep "test1.py" output.txt
grep "test3.py" output.txt

# Check if the output does not include .txt files
grep "test2.txt" output.txt
if [ $? -eq 0 ]; then
    echo "Test failed: test2.txt should not be included in the output"
    exit 1
fi
grep "test4.txt" output.txt
if [ $? -eq 0 ]; then
    echo "Test failed: test4.txt should not be included in the output"
    exit 1
fi

echo "Test passed"

# Clean up
rm -r "$TEMP_DIR"
rm output.txt
