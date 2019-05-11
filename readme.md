running code
```
install http://www.gambit-project.org/
uses python 2
pip install -r requirements.txt
```


building the book
```
uses ruby >= 2.30
http://rvm.io/ or brew install ruby
(for ubuntu)
sudo apt-get install ruby ruby-dev pkg-config libxslt-dev libxml2-dev


install https://asciidoctor.org

gem install asciidoctor
gem install asciidoctor-pdf --pre
gem install asciidoctor-pdf-cjk  # may not actually be needed after the switch to DejaVu

NOKOGIRI_USE_SYSTEM_LIBRARIES=1 gem install asciidoctor-epub3 --pre
```