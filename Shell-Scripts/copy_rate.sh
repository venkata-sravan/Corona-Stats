#! /bin/bash

sed -i '3,7d' change/*.html
sed -i '1d' change/*.html
sed -i '1 i <table border="1" class="dataframe" id="myTable">' change/*.html
sed -i '11,$ s/th/td/' change/*.html
sudo cp change/*.html /var/www/html/
