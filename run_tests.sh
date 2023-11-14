#!/bin/sh

if ! [ -f "tests/plots/" ]; then
    mkdir tests/plots
    echo "Created tests/plots/ directory"
fi

for t in $(ls tests/test*.py)
do
    echo "Running $t ..."
    pytest "$t"
done