# BUENOSAIRES PARSER

## INSTALL
Work only with python 3

Install the required packages:
```
pip3 install -r requirements.txt
```

## RUN

```
python3 main.py [options] [file in] [file out]
```
### OPTIONS
```
[file in] : filename of a un tagged acts XML file
[file out] : filename of the ouput tagged XML acts
[options] :
    -t : tag acts in filename_in into filename_out
    -N : use naive bayes classifier method
    -S : use linear SVC method
    -v : verbose mode
    -l [filename] : when tagging, use it to specify the file which contains learning set (tagged acts)
```

### EXAMPLES
Here the main use of this program : tag acts with naive bayes classifier.

Don't use linear SVC (bad results)
```
python3 main.py -t -N -l buenosaires.train.xml buenosaires.raw.xml buenosaires.tagged.xml
```

### GENERATE LEARNING SET
Learning set can be generate by extracting acts already tagged from all the acts.
```
python3 main.py -e buenosaires.raw.xml buenosaires.train.xml
```