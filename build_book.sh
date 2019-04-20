#!/bin/bash

asciidoctor book.txt
asciidoctor-pdf -a pdf-style=theme.yml -a pdf-fontsdir=fonts book.txt
