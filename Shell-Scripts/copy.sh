#! /bin/bash

sed -i '3,7d' *.html
sed -i '1d' *.html
sed -i '1 i <table border="1" class="dataframe" id="myTable">' *.html
sed -i '11,$ s/th/td/' *.html
sudo cp *.png /var/www/html/
sudo cp *.html /var/www/html/
