# Document-Classification-program

## Please Note

The input file must be in (.csv) format, with utf-8 encoding for the program to run.
For the program to run as intended, please set the last row in the file, to be the text of the document.



## About the programs

"computeARIintoANewLastColumn.py" computes the ARI score and readability level classification of the document, which will be added as 2 new columns in the output csv file. The output csv file contains the input csv data but with 2 new last column.

It also assumes the last column of the csv file to be the document text, and the document's text column is all it needs to calcuate its ARI score, and readability level classification.

<br />


"extract ten sentence.py" extracts around ten sentences from the last column of the input csv file. The output csv file of this program contains the input csv data but with its last row containing around 10 sentences extracted from its original text.



## Instructions to run



To run "computeARIintoANewLastColumn.py", open cmd in this program's directory, type into cmd:

"python computeARIintoANewLastColumn.py data_file.csv"

where data_file.csv can be changed to the name of the csv file u want the program to calculate the ARI with. 



<br /><br /><br />
 
For to run "extract ten sentence.py" too, , type into cmd:

"python extract ten sentence.py data_file.csv"

replace [data_file.csv] with the name of the csv file u want the program to extract around 10 sentences from.
