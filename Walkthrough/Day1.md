Before Class
----

Before you come tomorrow I need you to do three things:
 - Make a github account (github.com). Give some thought to your username as it will be the face of your professional work. Mine is dgasmith.
 - Make an account at projecteuler.net and solve at least one problem using Python. If you need any help ill be in the office.
 - Read (or at least skim) chapters 1.1 and 1.2 in the Scipy-Lecture notes (http://www.scipy-lectures.org). 

It is suggested that you get your python install through Anaconda (https://www.continuum.io/downloads). While we will use a standard suite of Python packages which can be obtained through other means Anaconda will allow easy access to high performance versions of these packages which will be quite useful before we dive into C++.


After Class
----

As a reminder please do 5 project Euler projects between problem 1 and 20, then upload them to GitHub and make pull request to the CDSG_SoC_2016 repository. The other piece of homework is to make sure to obtain python anaconda on your Ubuntu install for next week. If you have any issue please come find me, I will be at my desk.

GitHub tutorial for reference:
http://swcarpentry.github.io/git-novice/

Anaconda:
https://www.continuum.io/downloads

I also have two more documents for you to read. The first is a brief overview of NumPy and will start you on the long process of understanding vectorized computing. The second is some notes by Ed Valeev on general computer architecture.

https://docs.scipy.org/doc/numpy-dev/user/quickstart.html
http://www.valeevgroup.chem.vt.edu/docs/Intro2ComputerArchitecture4ComputationalScientists_2015.pdf


Further Comments
----

I am glad that progress is being made on ProjectEuler and Github. A few things to note that I have seen so far. 

First, examine Dom’s PR here:
https://github.com/dgasmith/CDSG_SoC_2016/pull/5

If you look into the “Files Changed” tab you will notice that he has begun to take advantage of the PyEuler library which can custom functions by you. In this case, he has efficiently implemented a Sieve of Eratosthenes algorithm for finding primes.


Second, examine Leonardo’s PR here:
https://github.com/dgasmith/CDSG_SoC_2016/pull/4/files#r64968279

In general we want to stick with the Pep8 style of Python coding (https://www.python.org/dev/peps/pep-0008/). The largest point I would like to make with this style for now is that we want to use exactly four spaces for indentation and _not_ tabs. To help you out you can add/set your “~/.vimrc” file to contain the following:

```
:syntax on
set tabstop=4
set shiftwidth=4
set expand tab
```

This notation will effectively expand a tab user input to four spaces making this part of the pep easy to accomplish. You can also run “pep8 file.py” if you installed conda to see how good or bad your code is adhering to this notation.

I highly suggest clicking “watch” in the top right corner of https://github.com/dgasmith/CDSG_SoC_2016 so that you can keep appraised of what everyone else is doing.
