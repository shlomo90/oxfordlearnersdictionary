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
