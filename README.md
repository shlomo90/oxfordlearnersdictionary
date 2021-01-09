# Oxfordlearnersdictionary

* Why make the program?
    * I got sick of searching words in browsers.
    * I use a terminal more than browsers. So. I need this program
      that has a terminal based interface dictionary which connects
      to the oxfordlearners dictionary website.
* How to work?
    * Use "requests" and "BeautifulSoup"
        * "BeautifulSoup" helps web scrapping.
* Who wants to use?
    * Some users working on a terminal more than Web Browsers.
    * Some users who are craving to learn English.


# How to use it?

1. Install virtualenv

```
pip install virtualenv
```

2. Generate virtualenv with python 2.7

* example

```
virtualenv -p /usr/bin/python2.7 dict
```

3. Activate virtualenv

```
source ./dict/bin/activate
```

4. Install dependency modules

```
pip install -r ./requirements.txt
```

5. Run program

```
./search word
```

# Examples

```
prompt$ ./search test ox
----------------------------------------------
Name           : test
Phonetic(br/am): /test/ /test/
----------------------------------------------
Short Cut: in cricket, etc.
Define: acricketor rugby match played between the teams of two different countries, usually as part of a series of matches on a tour
 - They played well in the first Test against South Africa.
 - He will be first choice for the opening test against the All Blacks.


Short Cut: of knowledge/ability
Define: an examination of somebody’s knowledge or ability, consisting of questions for them to answer or activities for them to perform
 - an IQ/a fitness test
 - a test on irregular verbs
 - a good mark in the test
 - a good score on the test


Short Cut: of health
Define: a medical examination to discover what is wrong with you or to check the condition of your health
 - screening tests for cancer
 - The pregnancy test was positive.


Short Cut: of strength, etc.
Define: a situation or an event that shows how good, strong, etc. somebody/something is
 - The local elections will be a good test of the government's popularity.
 - He saw their separation as a test of the strength of their love.
```
