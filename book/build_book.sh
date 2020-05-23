#!/bin/bash

asciidoctor unroll.adoc
asciidoctor-pdf -a pdf-style=theme.yml -a pdf-fontsdir=fonts unroll.adoc
asciidoctor-epub3 unroll.adoc
