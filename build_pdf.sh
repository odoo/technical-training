#!/bin/sh
pandoc Introduction.md 0*/README.md 10-reports/README.md --latex-engine=pdflatex -o "Technical Training.pdf" --variable urlcolor=blue -f markdown
