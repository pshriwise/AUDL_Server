pyultimate_stats
================

Contains python scripts for getting American Ultimate Disc League (AUDL) statistics information from the www.ultimate-numbers.com server.

Use
--------------

clone the repository using 

git clone https://github.com/pshriwise/CS638

in the top directory run the command:

python server.py


Documentation
--------------

In order to produce documentation for this application:

cd docs/

doxygen Doxyfile

To view the documentation via html:

open ./docs/html/index.html in your favorite browser


Testing
-------

To run tests for the AUDL server:

cd tests/

./run_tests

Note: An internet connection is currently required to run the tests!
