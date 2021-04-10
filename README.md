# !!! DRAFT - IN CONSTRUCTION !!! <!-- omit in toc -->
# A Systematical Approach To Identify Performance Issues <!-- omit in toc -->

Although each performance issue is unique, it is possible to identify their origin by following a systematical approach. A performance issue is generally located in the following topics:
* Servers configuration and network infrastructure (on-premise users)
* Odoo / PostgreSQL configuration  (on-premise users)
* Odoo custom code, and sometimes... the standard code :confused:

The first two topics are outside the scope of this document but, before going ahead, it's mandatory to **ensure your infrastructure is correctly configured** according to the number of concurrent users to support and your servers capabilities.

If the issue occurs in a production system, we strongly advise you to **reproduce the performance issue on a test system** with the exact same Odoo code, including custom addons, the same database structure and avoiding any reverse proxy and load balancer. This is necessary because very likely Odoo and PostgreSQL will be restarted during your investigations. Besides it will confirm the production infrastructure is not the root cause.
>**Note**: This document assumes you are using Linux. All system commands and tools mentioned may not be available in another operating system.

## Table Of Content <!-- omit in toc -->
- [Select a Use Case](#select-a-use-case)
- [Use the Web Browser Debugger](#use-the-web-browser-debugger)
- [Odoo or PostgreSQL](#odoo-or-postgresql)
- [Investigating Odoo](#investigating-odoo)
  - [Getting the PIDs of Odoo](#getting-the-pids-of-odoo)
    - [Using Odoo output](#using-odoo-output)
    - [Using system commands](#using-system-commands)
  - [Getting Stack Traces On The Fly](#getting-stack-traces-on-the-fly)
  - [Using py-spy](#using-py-spy)
    - [Install py-spy](#install-py-spy)
    - [Executing py-spy](#executing-py-spy)
    - [Analyzing a flamegraph](#analyzing-a-flamegraph)
- [Investigating PostgreSQL](#investigating-postgresql)
  - [Using PgActivity](#using-pgactivity)
    - [Installing PgActivity](#installing-pgactivity)
    - [Executing PgActivity](#executing-pgactivity)
  - [Using PgBadger](#using-pgbadger)
    - [Activate the query logging](#activate-the-query-logging)
    - [Installing PgBadger](#installing-pgbadger)
    - [Executing PgBadger](#executing-pgbadger)
    - [Analyzing a PgBadger report](#analyzing-a-pgbadger-report)
  - [Analyzing a SQL Query](#analyzing-a-sql-query)
- [When Everything Is Slow](#when-everything-is-slow)

## Select a Use Case
Most of the time we have to deal with a specific action that is running slowly: "*when I confirm this sale order*", "*when I open this tree view on this model*", "*when this cron is started*", ... The next chapters explain how to investigate a well defined use case.

If the use case occurs within a cron, jump to the chapter [Odoo or PostgreSQL](#odoo-or-postgresql). If you cannot identify a use case and you are rather feeling everything is slow, jump to the chapter [When Everything Is Slow](#when-everything-is-slow).

## Use the Web Browser Debugger
If the performance issue is not located in a cron, activate the debugger of your WEB browser before running your use case. In most browsers, this mode is activated with the F12 key .

>**Tips**: Discover all the power of the debugger in this talk: [Why the Browser's Debugger is a Backend Developper's Best Friend?](https://www.youtube.com/watch?v=-3UwhYe2HUw)

Once the debugger is activated, select the "Network" tab and run your use case. This will give you a first clue where the issue resides.

This example shows all the requests done by the WEB browser when loading the Applications menu.

![](/pics/network_appl_menu.png)

The load time of various assets is visible in the  columns "Time" and "Waterfall". You can identify which assets load slowly and you must investigate why. You may have customized some Javascripts... In this case you can stop reading this document and dive into the JS code.

When all the assets are subject to an unacceptable load time, check the **Filestore Access Time** in the chapter [When Everything Is Slow](#when-everything-is-slow).

In this next example, we have clicked on a menu item that opens a tree view on a model.

![](/pics/network_menu_view.png)

And this example shows a click on an action button.

![](/pics/network_button.png)

The method behind the button is visible in the "Request Payload" section of the "Headers" tab.

![](/pics/network_button_request.png)

Exploring the request of the slow actions will tell you where to start your investigations.

## Odoo or PostgreSQL
Most of the time the starting point of a performance issue is an action triggered by Odoo. But it doesn't mean Odoo is faulty. For example, Odoo can be slow because it's waiting for PostgreSQL responding to a query, and in this case the investigations must go on at the PostgreSQL side.
A simple way to identify "who is waiting for who ?" is to **measure the CPU activity of Odoo and PostgreSQL** during the use case.

With the command `top` you can measure the CPU activity of the processes `python` and `postgres`. In a *typical* activity, Odoo (the Python processes) may take around 70% of the CPU time, compared to 30% allocated to PostgreSQL. If you measure a CPU activity of PostgreSQL at, say 99%, you definitely have to take care of the [PostgreSQL server or database](#investigating-postgresql) first.
If, in the contrary, you measure the most CPU activity on a Python process, you have to look first at the [Odoo side](#investigating-odoo).
>**Note**: investigating PostgreSQL first does not exclude another cause of performance issue in Odoo, and vice-versa.

## Investigating Odoo
The principle is to check the stack of the Python processes launched by Odoo. It is thus necessary to first identify the PID of these processes. Then we will explain two methods of getting the stack traces: one inspecting it on the fly, another one using [py-spy](https://github.com/benfred/py-spy).
>*Note*: a third method consisting on profiling the code won't be explained as it requires source code modifications, hence guessing already  the potential location of the performance issue.

### Getting the PIDs of Odoo

#### Using Odoo output
The easiest way to get the PID of the Python processes is to check the beginning of the output of Odoo (stdout or log file). Here is an example of lines printed when Odoo is started with one worker HTTP and one worker Cron.
```
[timestamp] INFO [database] odoo.service.server: Worker WorkerHTTP (32618) alive
[timestamp] INFO [database] odoo.service.server: Worker WorkerCron (32621) alive
```
It means the client requests will be handled by the PID 32618, while the scheduled actions will be handled by the PID 32621.

There are as many lines **WorkerHTTP** as the number of workers set by the parameter **--workers**.
And there are as many lines **WorkerCron** as the number of workers set by the parameter **--max-cron-threads**.

#### Using system commands
You can also get the PIDs by inspecting the `odoo-bin` processes.
```
# ps -ef | grep odoo-bin

odoo     32411 32385  0 02:30 pts/2    00:00:01 path/to/python path/to/odoo-bin [options]
odoo     32618 32411  0 02:30 pts/2    00:00:00 path/to/python path/to/odoo-bin [options]
odoo     32619 32411  2 02:30 pts/2    00:00:04 path/to/python path/to/odoo-bin gevent [options]
odoo     32621 32411  0 02:30 pts/2    00:00:01 path/to/python path/to/odoo-bin [options]
```
You identify the master process PID 32411 that forked all others. PID 32619 is the `gevent` process, thus not a worker. PIDs 32618 and 32621 are the two target workers. But you need to know which is the worker HTTP and which is the worker Cron.

A simple way is to start a scheduled action manually and check which PID is running. You then get the PID of the worker Cron.

### Getting Stack Traces On The Fly
At any time you can use to command `kill -3 [worker pid]` to dump the stack trace of the worker to the output of Odoo (stdout or log file). If the stack trace often shows the same piece of code, you've located a starting point for your code investigation.

### Using py-spy
With [py-spy](https://github.com/benfred/py-spy), you continuously take snapshots of the stack trace of one Python process. So, you have to know the PID of the Odoo worker that will handle the requests triggered by your use case. The only way to know it in advance is to **start Odoo with one worker**.

If your **use case is a cron**, start Odoo with one worker Cron: **--workers=0 --max-cron-threads=1**. It is advised to deactivate all scheduled actions but the one to test. 

If your **use case is not a cron**, start Odoo with one worker HTTP: **--workers=1 --max-cron-threads=0**.

To make a correct analysis it is mandatory to **run py-spy during the complete execution of the use case**. You have to ensure the worker won't be recycled because it has reached its runtime limit. To do so, configure adequately the parameters `--limit-time-cpu` and `--limit-time-real`. Refer to [this documentation](https://www.odoo.com/documentation/14.0/reference/cmdline.html#multiprocessing) to know how to set these parameters.

#### Install py-spy
Follow the installation procedure from [https://github.com/benfred/py-spy](https://github.com/benfred/py-spy). A package may also be available for your distro. In Ubuntu, type the command:
```
# sudo apt-get install py-spy
```

#### Executing py-spy
Executing [py-spy](https://github.com/benfred/py-spy) will sample the Python stack and compile the result in a **flamegraph**. You can choose between a global flamegraph summarizing the stack during all the sampling period, or a flamegraph showing the evolution of the stack content during the use case. We will explain both formats.

- To get an overall picture of the Python stack, type the following command **before running the use case**:
```
# sudo py-spy record -o image.svg --pid [worker pid]
```
When the use case is complete, stop py-spy with `Ctrl-C`.

This will create a picture `image.svg` that is advised to open in a WEB browser because the content is clickable. Here is an example.

![](/pics/flamegraph_example_1.svg)

- To see the stack evolution over the time, ask py-spy to generate a report in the [speedscope](https://github.com/jlfwong/speedscope) format with the option `-f speedscope`.
```
# sudo py-spy record -f speedscope -o my_report --pid [worker pid]
```
This will generate the file `my_report` that you can upload on [https://www.speedscope.app](https://www.speedscope.app).

![](/pics/flamegraph_speedscope.png)

#### Analyzing a flamegraph

In a flamegraph, you see the hierachy of calls between methods. The longer the bar is, the more visible the method is in the stack, hence the more time is spent within the method. The color has no importance.

In this example, we explore the creation of account moves. We can see that the vast majority of the time is spent to recompute some computed fields. You have found a starting point for your investigations.

![](/pics/flamegraph_example_2.png)

## Investigating PostgreSQL
Assuming PostgreSQL is correctly configured, the principle here is to investigate all queries involved during the use case. As for Odoo we will explain how to do that on the fly with [PgActivity](https://github.com/dalibo/pg_activity) or by analysing PostgreSQL log files later with [PgBadger](https://github.com/darold/pgbadger).

### Using PgActivity
With [PgActivity](https://github.com/dalibo/pg_activity) you get a realtime view of the currently running, waiting or blocking queries on a selected PostgreSQL instance or database. You can even inspect queries remotely.

#### Installing PgActivity
Follow the installation procedure from [https://github.com/dalibo/pg_activity](https://github.com/dalibo/pg_activity). A package may also be available for your distro. In Ubuntu, type the command:
```
# sudo apt-get install pg-activity
```

#### Executing PgActivity
Run `pg_activity` as your PostgreSQL user.
```
# sudo su - postgres
# pg_activity [-p PORT] [-h HOST] [-d DBNAME]
```

Now run your use case. You should see by default the currently executed queries. Select the running, waiting or blocking queries with F1/F2/F3. Press the `-`or `+` key to change the refresh time.

![](/pics/pg_activity.png)

If you see a query taking *too much time* you've found a starting point of your investigations.

### Using PgBadger
[PgBadger](https://github.com/darold/pgbadger) analyzes the log files containing all processed queries and generates a comprehensive HTML report. This is much more comfortable than PgActivity for further analyzis.

First you have to configure PostgreSQL to log the queries.

#### Activate the query logging
Add the following lines at the end of the configuration file `postgresql.conf`.
```
log_destination = 'csvlog'
logging_collector = on
log_directory = '/var/log/postgresql/pg_log/'
log_filename = 'postgresql-%Y-%m-%d_%H%M%S.log'
log_min_duration_statement = 0
log_line_prefix = '%t [%p-%l] %q%u@%d '
log_file_mode = 0644
log_duration = on
log_lock_waits = on
log_checkpoints = on
```
The query log files will be located in `/var/log/postgresql/pg_log/`. Change it to your preferred location. The PostgreSQL user must have a Read/Write privilege in that folder. The log files will be generated in a CSV format, we will tell PgBadger to expect that format.

>*Note*: you can choose to log only queries that run longer than [x] millis with "log_min_duration_statement = [x]". With "0" we want to log all the queries. This could be annoying in the report but at least we are sure we don't miss any query.

Now restart PostgreSQL and run your use case. After a while you should see some `.csv` files in the `log_directory`.

#### Installing PgBadger
Follow the installation procedure from [https://github.com/darold/pgbadger](https://github.com/darold/pgbadger). A package may also be available for your distro. In Ubuntu, type the command:
```
# sudo apt-get install pgbadger
```

#### Executing PgBadger
Run `pgbadger` with specifying the `.csv` files to process and the CSV format.
```
# pgbadger /var/log/postgresql/pg_log/*.csv -f csv
```
This will generate a file `out.html` in your current folder. Open this file with a WEB browser.

![](/pics/pgbadger.png)

#### Analyzing a PgBadger report
At a first sight it worths walking through the whole report to inspect everything that would seem suspicious. One of the most valuable report is in the menu Top / Time Consuming Queries.

![](/pics/pgbadger_time_consuming.png)

You should inspect mainly two columns:
- **Times executed**: you should wonder if it's normal to have run this query so many times during the use case ? If not, you should probably reanalyze the business logic or refactor some code.
- **Avg duration**: if this time is *abnormally high* you can click on the "Examples" button to get a real query and analyze it with PostgreSQL. To get the explain plan of your query, go to the section [Analyzing a SQL Query](#analyzing-a-sql-query).

### Analyzing a SQL Query
Open a connection to your database, for example with `psql`, and type the command:
```
EXPLAIN ANALYZE [your query]
```
You get a detailled description on how the PostgreSQL optimizer performs the query.

![](/pics/explain_plan_raw.png)

You can paste the explain plan result in [https://explain.depesz.com/](https://explain.depesz.com/) to get more information on each operation.

![](/pics/explain_plan_depesz.png)

Each node is a link to the explaination of what is the node kind (Nested Loop, Hash, Seq Scan, ...).

As an example, a `Seq Scan` operation on a table with a high number of records is very likely a cause of performance issue. Adding a well chosen index in the related Odoo model is generally a good solution.

## When Everything Is Slow
 If you are globally experiencing a poor performance, **check your monitoring system**. The real cause is very likely visible on the reports.

 Please be aware of the following topics:
- **Network latency between servers**. This is especially important between the Odoo servers and the PostgreSQL server. If Odoo is hosted in a cloud, ensure all your servers are in the same physical location. You can measure the round trip time (RTT) between servers with the `ping` command. An RTT > 5 ms is weird.
- **Filestore access time**. In addition to attachements and pictures, the filestore hosts all the assets (Javascript and CSS files) that are constantly loaded when using the client application. A poor response time from the filestore location may have a drastical impact. From our experience, using a NFS mount point or an Amazon S3 bucket may cause performance issues. If these technologies cannot be avoided, consider [using a CDN](https://www.odoo.com/documentation/14.0/setup/cdn.html).
- **Too many sessions**. A high number of connections to Odoo leads to a high number of session files. These files ` werkzeug_*xxxxxxx*.sess` are stored in the folder `[Odoo data_dir]/sessions`. Upon each connection the sessions folder is listed, what can be time consuming, especially if the filestore is shared somehow. Despite the garbage collector of Odoo, if there are too many session files, consider a regular cleanup of the sessions folder or store them in a separate database using the module [session_db](https://github.com/odoo/odoo-extra/tree/master/session_db) (this module is unsupported).
- **PostgreSQL misconfigurations**. Even if PostgreSQL is correctly configured (ie. with [pgtune](https://pgtune.leopard.in.ua/#/)), you still have to ensure:
  - the database is vaccumed and the optimizer statistics are up to date: [https://www.postgresql.org/docs/current/sql-vacuum.html](https://www.postgresql.org/docs/current/sql-vacuum.html),
  - the automatic vaccum is correctly configured: [https://www.postgresql.org/docs/current/runtime-config-autovacuum.html](https://www.postgresql.org/docs/current/runtime-config-autovacuum.html).
- **Underrated server hardware**. As a quick reminder, a CPU frequency < 3GHz must be increased. SSD disks is a minimum asset.
- **Using virtualisation** is not recommended because of some overheads impacting the global performance, especially on the network and disk I/O throughputs. Check for any CPU or RAM over allocation and enable the [memory ballooning](https://en.wikipedia.org/wiki/Memory_ballooning) on the virtual machines.

