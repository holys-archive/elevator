Auto tweet [GDUFS movie information][1] to Sina Weibo

The code is ugly. I will refactor it !

Follow me in @weibo:  http://weibo.com/dpress


### How to start?


Make sure you have `python2.7`, `pip`, `virtualenv` installed.

    $ git clone https://github.com/holys/elevator.git
    $ cd elevator
    $ virtualenv venv
    $ source venv/bin/activate
    (venv) $ pip install -r requirements.txt


- Prepare database for storing history movie information

    sqlite3 /data/movie.db < schema.sql



[1]: http://strs.gdufs.edu.cn/web/
