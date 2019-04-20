install http://www.gambit-project.org/
uses python 2
python2 -m venv venv
pip install -r requirements.txt
source venv/bin/activate


install https://asciidoctor.org
uses ruby
gem install asciidoctor
gem install asciidoctor-pdf --pre
gem install asciidoctor-pdf-cjk  # may not actually be used after the switch to DejaVu