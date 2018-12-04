# Log Analysis

Udacity - Full Stack Web Developer Nanodegree - Databases with SQL and Python Project.

This project included 3 questions to solve it using python and SQL.

## Getting Started
This project used **Python 2.7.12** and **PostgreSQL** if you not install it yet you can follow step below to get that.

### Install VirtualBox
VirtualBox is the software that actually runs the virtual machine. [You can download it from virtualbox.org, here.](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1) Install the platform package for your operating system. You do not need the extension pack or the SDK. You do not need to launch VirtualBox after installing it; Vagrant will do that.

Currently (October 2017), the supported version of VirtualBox to install is version 5.1. Newer versions do not work with the current release of Vagrant.

### Install Vagrant
Vagrant is the software that configures the VM and lets you share files between your host computer and the VM's filesystem. [Download it from vagrantup.com.](https://www.vagrantup.com/downloads.html) Install the version for your operating system.

If Vagrant is successfully installed, you will be able to run `vagrant --version`
in your terminal to see the version number.

### Download the VM configuration
There are a couple of different ways you can download the VM configuration.

You can download and unzip this file: [FSND-Virtual-Machine.zip](https://s3.amazonaws.com/video.udacity-data.com/topher/2018/April/5acfbfa3_fsnd-virtual-machine/fsnd-virtual-machine.zip) This will give you a directory called FSND-Virtual-Machine. It may be located inside your Downloads folder.

Either way, you will end up with a new directory containing the VM files. Change to this directory in your terminal with `cd`. Inside, you will find another directory called **vagrant**. Change directory to the **vagrant** directory.

### Start the virtual machine
From your terminal, inside the **vagrant** subdirectory, run the command `vagrant up`. This will cause Vagrant to download the Linux operating system and install it. This may take quite a while (many minutes) depending on how fast your Internet connection is.

When `vagrant up` is finished running, you will get your shell prompt back. At this point, you can run `vagrant ssh` to log in to your newly installed Linux VM!

### SQL Data
Download SQL data [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) You will need to unzip this file after downloading it. The file inside is called `newsdata.sql`. Put this file into the `vagrant` directory, which is shared with your virtual machine.

To load the data, `cd` into the `vagrant` directory and use the command
```bash
psql -d news -f newsdata.sql
```

## How to run program

```bash
python LogAnalysis.py
```

## Author
* Dejnarong Lamleangpon - _Programmer_ - [Profiles](https://github.com/Dejnarong)


## Program's design
### Functions
* Connect()
  * I design this function to connect `psql` and query data and than display in format.
  * This function use `cursor` to execute string of `sql query` to get data

    ```python
        db = psycopg2.connect(database=DBNAME) #connect to db (psql)
        cur = db.cursor()
        try:
         cur.execute("""select * from log limit 100;""")
        except psycopg2.Error as e:
         pass
    ```
  * Using `fetchall()` to get all of data rows and than use `for loop` to display them in format.

    ```python
      rows = cur.fetchall() #keep query data to rows
      for row in rows: #loop to display
        str_result = "{} -- {} views".format(row[2], row[0]) #format data
        print(str_result) #display
    ```
### SQL Queries
* Question 1 - What are the most popular three articles of all time?
  * I used `left join` **table articles** and **table log** for this question

    ```sql
     select articles.title as article_name,count(log.path) as views
     from log
     left join articles
     on log.path like concat('%',articles.slug) -- left join to get article title.
     where status like '%200%' and log.path like '/article/%' -- filter data only success and not home page.
     group by log.path,articles.title
     order by views desc limit 3; --get only top 3
    ```   
* Question 2 - Who are the most popular article authors of all time?
  * I modified from **question 1** but add one more `left join` for get the author names.   
    
    ```sql
     select count(log.path) as views,articles.author,authors.name --get views of article with author name
     from log.
     left join articles --first left join for get views of article.
     on log.path like concat('%',articles.slug) --like a question 1
     left join authors --second left join for get author name of article.
     on articles.author = authors.id
     where status like '%200%' and log.path like '/article/%' --like a question 1.
     group by articles.author,authors.name
     order by views desc;
    ```   
* Question 3 - On which days did more than 1% of requests lead to errors?
  * I used `sub query` and `left join` to get data in this question.

    ```sql
      select * --main select to get rows of data about more than 1% error.
      from (select TO_CHAR(main.d, 'Mon DD, YYYY') --this subquery is get percent of error request by date from next sub query.
            ,main.errortrans,main.alltrans
            ,(cast(errortrans as float) / cast(main.alltrans as float) * 100.0) as percents
            from (select cast(time as date) as d,count(status) as alltrans,e.errortrans --this sub query is get total of success request and errror request to calculate percent on above query.
                  from log
                  left join (select cast(time as date) as edate,count(status) as errortrans --this sub query is get total of error request by date.
                             from log 
                             where status like '4%' --Error request will have status code 4xx
                             group by cast(time as date)) as e
                  on cast(time as date) = e.edate
                  group by cast(time as date),e.errortrans ) as main) as result
       where result.percents > 1.0; -- get only data error more than 1% here.
    ```

## Acknowledgments
  * Some installation guide (links / information) are taken from what I learned in the udacity course.