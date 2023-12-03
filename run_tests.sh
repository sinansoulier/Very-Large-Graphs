#!/bin/sh

PLOT_DIR=./tests/plots

if [ -d "$PLOT_DIR" ]; then
    rm -rf "$PLOT_DIR"
    echo "Removed $PLOT_DIR directory"    
fi

mkdir "$PLOT_DIR"
echo "Created $PLOT_DIR directory\n"

for t in $(ls tests/test*.py)
do
    echo "Running $t ..."
    python -m pytest "$t"
done