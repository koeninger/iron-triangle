Unroll is a tabletop roleplaying game based on simultaneous choice, not random die rolls.

Read the book at [book/unroll.pdf](book/unroll.pdf),  [book/unroll.epub](book/unroll.epub) or [book/unroll.html](book/unroll.html)

Printable card deck at [book/deck.pdf](book/deck.pdf)


building the book
```
install ruby >= 2.4

(for osx)
brew install ruby or
http://rvm.io/
rvm install 2.6
source ~/.rvm/scripts/rvm
rvm use --default 2.6

brew install libxml2 libxslt libiconv
NOKOGIRI_USE_SYSTEM_LIBRARIES=1 gem install nokogiri -- --use-system-libraries --with-iconv-dir="$(brew --prefix libiconv)" --with-xml2-config="$(brew --prefix libxml2)/bin/xml2-config" --with-xslt-config="$(brew --prefix libxslt)/bin/xslt-config"

(for ubuntu)
sudo apt-get install ruby ruby-dev pkg-config libxslt-dev libxml2-dev


install https://asciidoctor.org

gem install asciidoctor
gem install asciidoctor-pdf --pre
gem install asciidoctor-pdf-cjk  # may not actually be needed after the switch to DejaVu
NOKOGIRI_USE_SYSTEM_LIBRARIES=1 gem install asciidoctor-epub3 --pre

cd book
./build_book.sh

asciidoctor may spit out errors, but as long as it builds the pdf it worked...
```

building the deck

http://www.nand.it/nandeck/

see book/deck.txt


running code (for game theory, this is a tabletop game not a video game)
```
install http://www.gambit-project.org/
build the python extension, e.g. http://www.gambit-project.org/gambit15/build.html#build-python

uses python 2
pip install -r requirements.txt
cd code

(assumes osx with gambit in /Applications)
gambit.sh
python graph.py
```


Copyright 2019 Loren Cody Koeninger.

This work is licensed under a [Creative Commons Attribution-NonCommercial 4.0 International License](http://creativecommons.org/licenses/by-nc/4.0/).
