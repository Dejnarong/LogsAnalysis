# My Log Analysis (Databases with SQL and Python Project)

This project included 3 questions to solve it using python and SQL.

## Pre Installation

### Install Python
See how to install pytron [here](http://www.pyladies.com/blog/Get-Your-Mac-Ready-for-Python-Programming/)

### SQL
Download SQL data [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) You will need to unzip this file after downloading it. The file inside is called `newsdata.sql`. Put this file into the `vagrant` directory, which is shared with your virtual machine.

To load the data, `cd` into the `vagrant` directory and use the command
```bash
psql -d news -f newsdata.sql
```

## How to run program

```bash
python LogAnalysis.py
```

## Program's design
I use `left join` to query the result and use python to display look like example.
Sorry about my english.