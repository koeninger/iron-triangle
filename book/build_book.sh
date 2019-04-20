#!/bin/bash

asciidoctor iron_triangle.adoc
asciidoctor-pdf -a pdf-style=theme.yml -a pdf-fontsdir=fonts iron_triangle.adoc
asciidoctor-epub3 iron_triangle.adoc
