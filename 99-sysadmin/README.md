# Odoo Deployment & Performance

## Goal

The aim of this training is to give good practice to deploy and maintain an odoo deployment, using a Linux system, 
for small business to bigger ones, from one system with multiple odoo to one odoo on multiple systems.

We'll also deploy tools to monitor server, track performance bottleneck, ...

There's many ways to deploy odoo, from a .deb on a virtual machine to multiple docker containers, 
from a self hosted server to a cloud instance. We'll use the recommended way to use a less layers as possible, 
as every layer you add require to master it.

## Schedule

| Day 1               | Day 2                     |
| ------------------- | ------------------------- |
| Install PostgreSQL  | Adanced NGinx             |
| Install Odoo        | PostgreSQL Configuration  |
| Install NGinx       | Data Replication          |
| Odoo Configuration  | Load balancing            |
| Odoo command line   | Etherpad                  |
| Exercices           | Backup                    |
|                     | Monitor                   |

## The Odoo architecture

From the web browser to PostgreSQL, many layers interact with other ones to process datas.

Inline-style: 
![Odoo architecture layers](./img/odooarch.png )

### One server

Easy to understand and deploy, it's the most common case. 1 instance or multiple instances

![Odoo architecture layers](./img/workers.png )

![Odoo architecture layers](./img/oneservermultipleodoo.png )

### Multiple servers

Harder to deploy and maintain, require higher sysadmin skills, recommended for fault tolerance and larger business.

![Odoo architecture layers](./img/oneodoomultipleserver.png )

### And a mix

Between those two configurations, there's plenty of deployment scenarios, depending on the needs. 
Always remember that you'll need a production system, and a testing system.

Testing system does not have to be the same that the production one, but must use same architecture (OS, ...).

Don't use a shared server between test and production env, to avoid performance bottleneck while testing, 
permit a restart on test without stopping production, ...

## KISS

> Keep it stupid and simple

Remember that you need a stable and maintainable system. Every layer you add require knowledge. 
Don't add unnecessary layers. En example can be a replicated database with nobody able to monitor it 
or easy recover from a failure, causing a bigger downtime in case of failure than in a single server scenario.

# Small system requirements

You've received many virtual machines, with Ubuntu 16.04 installed with a running SSH server, like you've received
if you had ordered a machine in a data center. All thoses machines are configured to connect each others using a
192.168.56.x private network.

You should configure this private network within VirtualBox and set 192.168.56.1 as your machine ip address within
this private network.

![Odoo architecture layers](./img/addprivatenet.png )

## SSH

Make server available by ssh with key authenticationMake server available by ssh with key authentication. You should :

* Allow users to use key authentification
* permit dsa keyspermit dsa keys

```bash
$ sudo vi /etc/ssh/sshd_config
```

```apacheconf
AuthorizedKeysFile      %h/.ssh/authorized_keys
PubkeyAcceptedKeyTypes ssh-dss
```

## Have SSH keys

Github require user authentication for private repositories (enterprise). As using https require to enter 
user/password for every fetch, it's easier to use ssh auth with github.

You can choose to use dsa or rsa, the key must be added to your github account, and must be password protected.

```bash
$ ssh-keygen -t rsa -N odoo!
```

## Some required tools

We'll need some tools to check system, like htop for process checking, git for cloning odoo sources, iotop 
and systat to check I/O. Others will be installed later when necessary.

```bash
$ sudo apt-get install git htop iotop sysstat
```

## Fix locale issue

You've maybe seen a locale issue when performing some commands like apt. This can simply be fixed by adding the required ones.

```bash
$ sudo locale-gen "en_US.UTF-8"
$ sudo dpkg-reconfigure locales
$ export LC_ALL="en_US.UTF-8"
$ sudo vi /etc/environment
```

```conf
PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games"
LC_ALL=en_US.UTF-8
LANG=en_US.UTF-8
```

# Install PostgreSQL

## Use apt.postgresql.org

You can choose to use the distribution repo to install PostgreSQL, or the official PostgreSQL apt repository to install 
a more recent version of PostgreSQL. Ubuntu has only one PostgreSQL version per release in official repo. 
We'll use the PostgreSQL one here.

```bash
$ wget https://anonscm.debian.org/cgit/pkg-postgresql/postgresql-common.git/plain/pgdg/apt.postgresql.org.sh
$ sudo bash apt.postgresql.org.sh
```

## Install PostgreSQL

You'll need the postgresql server itself, the client lib, and pg-activity to check running queries on a real-time basis.

```bash
$ sudo apt-get install postgresql-9.6 postgresql-client-9.6 \
   postgresql-client-common postgresql-common \
   postgresql-server-dev-9.6 pg-activity
```

A PostgreSQL user is required by Odoo to connect. For now, we'll use same PostgreSQL username as the unix one to use unix socket.

```bash
$ sudo su - postgres
postgres> psql
postgres=# CREATE USER odoo WITH LOGIN CREATEDB;
postgres=# \q
postgres> exit
$
```

PostgreSQL is now up and running

# Install Odoo

We'll deploy Odoo from git sources

Why using git instead of .deb?

* Better control on which version to deploy (per commit basis)
* Easier to download than the enterprise deb file
* No need to wait the nigthly build for a bug fix
* Other packages, like community ones, are easily available this way

## git clone

We'll use /opt/odoo10 as base dir.

```bash
$ cd /opt
$ sudo mkdir odoo10
$ sudo chown odoo odoo10
$ cd odoo10
$ git clone git@github.com:odoo/odoo.git
   OR
$ git clone -b 10.0 --single-branch git@github.com:odoo/odoo.git
```

The next one require enterprise access

```bash
$ git clone git@github.com:odoo/enterprise.git
```

## Odoo prerequisites

Odoo have some required python packages (like the web server, db connection library, ...). Those python packages needs 
some C/C++ headers to compile. We install the required C/C++ dev libraries from distribution repo, then we use pip 
to install the Odoo python required packages.

** Odoo is running on CPython 2.7! **

```bash
$ sudo apt install python-pip libxml2-dev libxslt-dev libjpeg-dev \
   libjpeg8-dev libpng-dev libldap2-dev libsasl2-dev node-less
$ cd /opt/odoo10/odoo
$ sudo pip install pip --upgrade
$ sudo pip install -r requirements.txt --upgrade
```

## First launch

We can now launch odoo to check if all is ok and create a first database. We've deployed all required dependencies, 
we'll just use one option on the command line to explain where we can find addons. Enterprise addons are set before 
the community ones!

```bash
$ cd /opt/odoo10/odoo
$ ./odoo.py --addons-path=/opt/odoo10/enterprise,/opt/odoo10/odoo/addons
```

Hit CTRL+C twice to stop the server.

## WKHtmlToPdf

To print reports, odoo generates an html, send it to wkhtmltopdf which is in charge of the html->pdf transformation.

```bash
$ sudo apt install libxrender1 fontconfig
$ wget http://nightly.odoo.com/deb/xenial/wkhtmltox-0.12.1_linux-trusty-amd64.deb
$ sudo dpkg -i wkhtmltox-0.12.1_linux-trusty-amd64.deb
```

# NGinx

## Install NGINX

```bash
$ sudo apt-get install nginx
```

We'll assume that our server name is odoo.training.internal, and that our DNS is well configured to handle this.

We'll also need other aliases **pad.training.internal** and **community.training.internal**

Locally, for training purpose, we can simply modify our hosts file.

## A small config later

```bash
$ sudo vi /etc/nginx/sites-available/odoo
```

```apacheconf
#odoo server
upstream odoo {
    server 127.0.0.1:8069;
}

server {
    listen 80;
    server_name odoo.training.internal;

    # Add Headers for odoo proxy mode
    proxy_set_header X-Forwarded-Host $host;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header X-Real-IP $remote_addr;

    #log
    access_log /var/log/nginx/odoo.access.log;
    error_log /var/log/nginx/odoo.error.log;

    # Redirect requests to odoo backend server
    location / {
      proxy_redirect off;
      proxy_pass http://odoo;
    }
}
```

Re-Launch NGINX

```bash
$ sudo ln -s /etc/nginx/sites-available/odoo /etc/nginx/sites-enabled/odoo
$ sudo /etc/init.d/nginx restart
$ ./odoo.py --proxy-mode \
   --addons-path=/opt/odoo10/enterprise,/opt/odoo10/odoo/addons
```

Odoo Seems to run behind NGINX. Proxy-mode because odoo is behing nginx. Forwarded headers are very important because 
Odoo only see 1 client : nginx!

Check the logs and you'll see only 1 ip : 127.0.0.1

## Odoo as a service

using Systemd, we'll start odoo at system staretup.

```bash
$ sudo vi /lib/systemd/system/odoo.service
```

```
[Unit]
Description=odoo
Requires=postgresql.service
After=postgresql.service
Wants=nginx.service

[Install]
Alias=odoo.service

[Service]
Type=simple
User=odoo
Group=odoo
SyslogIdentifier=odoo-server
PIDFile=/run/odoo/odoo-server.pid
ExecStart=/opt/odoo10/odoo/odoo.py --config=/etc/odoo/odoo10.conf

[Install]
WantedBy=multi-user.target
```

**If PostgreSQL is on another host**

```
[Unit]
After=network.target
```

```bash
$ sudo mkdir /etc/odoo
$ sudo chown odoo /etc/odoo
$ sudo mkdir /var/log/odoo
$ sudo chown odoo /var/log/odoo
$ vi /etc/odoo/odoo10.conf
```

```
[options]
addons_path = /opt/odoo10/enterprise,/opt/odoo10/odoo/addons
proxy_mode = True
```

```bash
$ sudo systemctl start odoo
$ sudo systemctl enable odoo.service
```

Now it seems working, even after a system restart.

# Configure Odoo

## Add logging

By default, Odoo displays all logging of level info except for workflow logging (warning only), and log output is sent to stdout

```bash
$ sudo chown odoo /var/log/odoo
$ sudo chgrp odoo /var/log/odoo
```

```
[options]
addons_path = /opt/odoo10/enterprise,/opt/odoo10/odoo/addons
proxy_mode = True
logfile = /var/log/odoo/odoo.log
syslog = False
log_db = False
```

## Log rotation

In some cases, it's not a good idea to use the odoo log rotation internal mechanism, because 2 workers can try to rotate logs at the same time.

To achieve such a goal, we use the logrotate daemon.

```
[options]
...
logrotate = False
```

```bash
$ sudo apt install logrotate
$ sudo vi /etc/logrotate.d/odoo
```

```
/var/log/odoo/odoo.log {
    rotate 10
    daily

    # Do not rotate the log if it is empty
    notifempty

    # if the log file is missing, go on to the next one without
    # issuing an error message.
    missingok

    compress
    delaycompress
}
```

## Check logs

As logs are sent to a file, here's how to display them in real-time

```bash
$ tail -f /var/log/odoo/odoo.log
```

To search within the log, for a regex, and display line number, 2 lines after and 5 lines before the result

```bash
$ grep -n Worker.*unregistered /var/log/odoo/odoo.log -A2 -B5
```

## Log handler

the log handler is a list of logger/level combination. If logger is omitted, the root logger is used. Level is a 
choice between INFO, WARNING, CRITICAL and DEBUG

```
[options]
...
log_handler = openerp.sql_db:DEBUG,werkzeug:DEBUG,openerp.fields:WARNING,openerp.http.rpc.request:DEBUG,:WARNING
```

This handler will

* Debug sql queries
* Debug werkzeug queries
* Warn openerp.fields module
* Debug RPC queries
* Warn on others

## Log level

log levels are shortcut for log handlers, to ease configuration of most commonly used handlers combination : critical, error, warn, debug, debug_sql, debug_rpc, debug_rpc_answer

```
[options]
...
log_level = debug_rpc
```

## Odoo workers

* Only on unix
* Python GIL: in CPython, the global interpreter lock, or GIL, is a mutex that prevents multiple native threads from executing Python bytecodes at once.

![Odoo architecture layers](./img/workers.png )

### Add workers

* 1 worker ~= 6 users
* \# workers = (\#cpus * 2 ) + 1
```
[options]
...
workers = 4
max_cron_threads = 1
```

Check in log :

* openerp.service.server: Evented Service (longpolling) running on 0.0.0.0:8072
* Exception: bus.Bus unavailable

### Nginx with workers

As the longpolling is on another tcp port, we must forward /longpoll/ request to the correct port. 
Don't forward all requests to this port, or you'll never user the workers process

```
[...]
upstream odoo_longpoll {
 server 127.0.0.1:8072;
}
[...]
location /longpoll {
   proxy_redirect off;
   proxy_pass http://odoo_longpoll;
 }
[...]
```

### Check process list with/without workers

![Odoo architecture layers](./img/processlist.png )

### Workers limits

Odoo process are recycled, on a parametrized basis.

#### CPU

* limit_time_cpu = 60
* limit_time_real = 120
* limit_time_real_cron = limit_time_real    **New since V10**

If a worker reach the limit, the process is killed, without sending the response to the client. 

It's important to set to a high enough value.

#### Memory
**limit_memory_soft = 2 Gb**

A worker which reach this memory limit during the processing of the request is recycled after sending the response.

**limit_memory_hard = 2.5 Gb**

A worker which reach this memory limit during the processing of the request is recycled immediatly, without sending the response.

#### Requests count

**limit_request = 8192**

 A worker which process this # of request is recycled at the end of the request response

#### Set workers limits

```
[options]
...
limit_time_cpu = 60
limit_time_real = 240
limit_time_real_cron = 3600
limit_memory_soft = 2147483648
limit_memory_hard = 4294967296
limit_request = 8192
```

Test workers recycling, soft and hard... You can set for example, limit_request to 2 or any other stupid value

```
INFO tst1 openerp.service.server: Worker (3120) max request (8192) reached.
INFO tst1 openerp.service.server: Worker (3120) exiting. request_count: 8192, registry count: 1.
DEBUG ? openerp.service.server: Worker (3120) unregistered
INFO ? openerp.service.server: Worker WorkerHTTP (3129) alive
```

## Wizard limits

Wizard are object defined as not-persistent within Odoo. Those objects are in fact stored within the database and 
cleaned with a cron. By default, cron clean those records after one hour. You can choose to clean faster/slower and/or 
limit the number of such records within the database.

**osv_memory_count_limit** is a per table setting, while **osv_memory_age_limit** (expressed in **hours**) is for all wizards.

```
[options]
...
osv_memory_count_limit = 100000
osv_memory_age_limit = 4
```

## DB Filtering

When using website, it's required to use db filtering. dbfilter is a regex, which can contain %d and %h special values, representing respectively the server name and the FQDN.

**dbfilter**
* regex
* %h
* %d

```
...
dbfilter = ^%d[0-9]*$
```

## DB admin

Avoid anyone to drop your db's, stole your datas,... via /web/database/manager

**admin_passwd**

```
 $ python -c 'import base64, os; print(base64.b64encode(os.urandom(24)))'
```

```
...
admin_passwd = ApRmoGy+DcFREAVCkD7PbtznKc1KDsyU
```

## DB Connection

Manage connection to the server. Using uniw sockets by default (or localhost on windows)

db_maxconn is a per-worker limit

```
[options]
...
db_name = False
db_host = False
db_port = 5432
db_user = False
db_password = False
db_template = template1
db_maxconn = 4
```

## List DB

By default, a user can choose db to connect to. list_db can disable this feature.

```
[options]
...
list_db = False
```

## Unaccent & geoip_database

Use the unaccent function provided by the database when available.

geoip_database is a free database of IP geolocalisation.

```
[options]
...
unaccent = False
geoip_database = /usr/share/GeoIP/GeoLiteCity.dat
```

## Data dir

Some binaries are stored on the file system, instead of storing them in DB. Default is 
home_drive/.local/share/odoo/version, C:\\Documents and Settings\\<User>\\Application Data\\... on Windows, ...

```
[options]
...
data_dir = /home/odoo/datas
```

**Don't forget to backup it!**

## IP ports

You can change the ip ports used

```
[options]
...
xmlrpc = True
xmlrpc_interface = 127.0.0.1
xmlrpc_port = 8069
longpolling_port = 8072
```

## SMTP

You can configure a default mail server. By default, Odoo use localhost on port 25, without SSL nor authentication

```
[options]
...
email_from = nse@training.internal
smtp_server = 127.0.0.1
smtp_port = 25
smtp_ssl = False
smtp_user = False
smtp_password = False
```

## Demo data

It's better on production server to avoid deploying demo datas... (comma-separated, use \\"all\\" for all modules) Used with -d and -i

```
[options]
...
without_demo = all
```

## Debug mode

Known from Odoo developers, this mode alter a bit the datadriven mode of Odoo, by reading files from disks instead of database

```
[options]
...
debug_mode = False
```

## Big imports

Use this for big data importation, if it crashes you will be able to continue at the current state. Provide a filename to store intermediate importation states.

```
[options]
...
import_partial = /user/odoo/tempimport
```

## Pid File

Store the pid within a file

```
[options]
...
pidfile = /run/odoo/odoo-server.pid
```

Let systemd storing pidfile

```
[options]
...
pidfile = False
```

## Server wide modules

server-wide modules are supposed to provide features not necessarily tied to a particular database. By default, only /web

```
[options]
...
server_wide_modules = web,mysupermodule
```

A use case for those kind of modules are the hw_xxx modules of the posbox

# Per-DB Odoo Configuration

## ir.config_parameter

It's possible to change some settings on a per-database basis. Those parameters permit to solve some issues 
depending on the deployment senario.

The most frequent ones are web.base.url.freeze and report.url

## web.base.url

**web.base.url** is the base url of your Odoo deployment. You can change it in the ir.config_parameter table. 
The default behaviour of Odoo is to reset the value of this parameter each time the admin logs in. 
Logging in with admin using an ssh tunnel can broke some features...

If parameter **web.base.url.freeze** is set, this behaviour is disabled.

## pdf reports

Here are the steps when odoo prints a pdf:

* Odoo generates an html
* Odoo send the html to wkhtmltopdf
* wkhtmltopdf request assets to Odoo
* wkhtmltopdf transform html into pdf
* wkhtmltopdf send pdf to Odoo
* Odoo sends pdf to the browser

### report.url

wkhtmltopdf can request informations (assets) directly from Odoo, without contacting reverse proxy. 
In some scenarios, when web.base.url is resolved as the firewall ip for example, the firewall detects a software in the 
lan requesting an url in the lan, then drop the request. This makes the wkhtmltopdf request for assets fails, and thus 
the generated pdf lacks of css.

the report.url can be set to _ http://localhost:8069 _ to enable direct connection from wkhtmltopdf to Odoo.

# Other Odoo command line operations

## Perform a full update

```bash
$ cd /opt/odoo10/odoo
$ git pull
$ cd /opt/odoo10/enterprise
$ git pull
$ sudo service odoo stop
$ cd /opt/odoo10/odoo
#comment out logfile in config
$ ./odoo.py -c /etc/odoo/odoo10.conf -d mydb -u all --stop-after-init
$ sudo service odoo start
```

### Avoid lack of log

The idea is to remove the logfile from config, add it to startup script, to ease the update process

in /etc/odoo/odoo10.conf :

```
#logfile = /var/log/odoo/odoo.log
```

in /lib/systemd/system/odoo.service :

```
ExecStart=/opt/odoo10/odoo/odoo.py --config=/etc/odoo/odoo10.conf --logfile /var/log/odoo/odoo.log
```

```
$ sudo systemctl daemon-reload
$ sudo systemctl stop odoo
$ sudo systemctl start odoo
```

## Install a module in command line

```
$ ./odoo.py -c /etc/odoo/odoo10.conf -d mydb -i mymodule --stop-after-init
```

# Exercices

## 2 instances

Without altering the running server, it's asked to deploy as a service, and only accessible through NGinx:

| Workers, cron | FQDN                     | DB filter | Ports      | Edition
| ------------- | ------------------------ | --------- | ---------- | ---------
| 3, 2          | odoo10.training.internal | odoo10*c  | 9069, 9072 | community
| 2, 2          | odoo10.training.internal | odoo10*c  | 9069, 9072 | community

## 1 instance, 2 customers

Without altering the running servers, it's asked to deploy as a service, and only accessible through NGinx, one odoo 10 enterprise serving two customers, with 3 workers and 1 cron, on ports 8079 and 8082:

| FQDN	| DB
| ----- | ---
| cust1.training.internal | cust1
| cust2.training.internal | cust2

## Logging

Set logging on cust1 to debug the rpc responses.

Set logging on cust2 to debug the rpc queries, debug sql queries, and only critical on others.

Set logging on the odoo9 instance to debug only the crm module, and info on others.

## New module

On the Odoo9 instance, deploy one OCA module, accessible through github, and install it on database.

# Advanced NGINX

## SSL

For now, Odoo is running in clear http. We need to redirect http requests to https ones.

```
proxy_set_header X-Forwarded-Host $host;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Proto $scheme;
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header Host $http_host;
add_header X-Content-Type-Options nosniff;

# http -> https
server {
   listen 80;
   server_name odoo.training.internal;

   rewrite ^(.*)$ https://$host$1 permanent;
}
```

And we need to handle https requests

```
#SSL
server {
    listen 443;
    server_name odoo.training.internal;

    ssl on;
    ssl_certificate /etc/ssl/nginx/server.crt;
    ssl_certificate_key /etc/ssl/nginx/server.key;
    ssl_session_timeout 30m;
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
    ssl_ciphers 'ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:DHE-DSS-AES128-GCM-SHA256:kEDH+AESGCM:ECDHE-RSA-AES128-SHA256:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA:ECDHE-ECDSA-AES128-SHA:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA:ECDHE-ECDSA-AES256-SHA:DHE-RSA-AES128-SHA256:DHE-RSA-AES128-SHA:DHE-DSS-AES128-SHA256:DHE-RSA-AES256-SHA256:DHE-DSS-AES256-SHA:DHE-RSA-AES256-SHA:AES128-GCM-SHA256:AES256-GCM-SHA384:AES128-SHA256:AES256-SHA256:AES128-SHA:AES256-SHA:AES:CAMELLIA:DES-CBC3-SHA:!aNULL:!eNULL:!EXPORT:!DES:!RC4:!MD5:!PSK:!aECDH:!EDH-DSS-DES-CBC3-SHA:!EDH-RSA-DES-CBC3-SHA:!KRB5-DES-CBC3-SHA';
    ssl_prefer_server_ciphers on;

    [...]
```

## Pos

If you're using posbox, as the browser connect to the posbox using http, you've to publish the pos using http
to avoid a mixed content error within the browser.

```
server {
  listen 80;
  [...]
  #Redirect non-POS and related content in https to allow POS in http
  location ~ ^(?!/pos/|/web/binary/company_logo|/?[^/]*/website/action/|/web/webclient/|/web/content/|/web_editor/static/|/web/css/|/web/static/|/point_of_sale/static).*$ {
      proxy_redirect off;
      if ($request_method != POST) {
        # rewriting a POST request has no sense as the browser will do the request as GET
        rewrite ^(.*)$ https://$host$1 permanent;
      }
      if ($request_method = POST) { proxy_pass http://odoo; }
   }

   location = /longpolling/poll { proxy_redirect off; proxy_pass http://odoo_longpoll;}
   location / { proxy_redirect off; proxy_pass http://odoo; }
}
[...]
server {
  listen 443;
  [...]
  # Redirect POS to http
 location ~ ^/pos/web {
   rewrite ^(.*) http://$host:80$1 permanent;
 }
 # Redirect requests to odoo backend server
 location / {
   proxy_redirect off;
   proxy_pass http://odoo;
 }
 location /longpolling {
   proxy_redirect off;
   proxy_pass http://odoo_longpoll;
 }
}
```

## Full NGinx config

```
#odoo server
upstream odoo {
 server 127.0.0.1:8069;
}
upstream odoo_longpoll {
 server 127.0.0.1:8072;
}

proxy_set_header X-Forwarded-Host $host;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Proto $scheme;
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header Host $http_host;
add_header X-Content-Type-Options nosniff;

server {
  listen 80;
  server_name odoo.training.internal;

  access_log /var/log/nginx/odoo.access.log;
  error_log /var/log/nginx/odoo.error.log;

  #Redirect non-POS and related content in https to allow POS in http
  location ~ ^(?!/pos/|/web/binary/company_logo|/?[^/]*/website/action/|/web/webclient/|/web/content/|/web_editor/static/|/web/css/|/web/static/|/point_of_sale/static).*$ {
      proxy_redirect off;

      if ($request_method != POST) {
        # rewriting a POST request has no sense as the browser will do the request as GET
        rewrite ^(.*)$ https://$host$1 permanent;
      }
      if ($request_method = POST) {
        proxy_pass http://odoo;
      }
   }
  location = /longpolling/poll {
     proxy_redirect off;
     proxy_pass http://odoo_longpoll;
   }

  location / {
     proxy_redirect off;
     proxy_pass http://odoo;
   }
}

server {
 listen 443;
 server_name odoo.training.internal

 access_log /var/log/nginx/odoossl.access.log;
 error_log /var/log/nginx/odoossl.error.log;

 # SSL parameters
 ssl on;
 ssl_certificate /etc/ssl/nginx/server.crt;
 ssl_certificate_key /etc/ssl/nginx/server.key;
 ssl_session_timeout 30m;
 ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
 ssl_ciphers 'ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:DHE-DSS-AES128-GCM-SHA256:kEDH+AESGCM:ECDHE-RSA-AES128-SHA256:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA:ECDHE-ECDSA-AES128-SHA:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA:ECDHE-ECDSA-AES256-SHA:DHE-RSA-AES128-SHA256:DHE-RSA-AES128-SHA:DHE-DSS-AES128-SHA256:DHE-RSA-AES256-SHA256:DHE-DSS-AES256-SHA:DHE-RSA-AES256-SHA:AES128-GCM-SHA256:AES256-GCM-SHA384:AES128-SHA256:AES256-SHA256:AES128-SHA:AES256-SHA:AES:CAMELLIA:DES-CBC3-SHA:!aNULL:!eNULL:!EXPORT:!DES:!RC4:!MD5:!PSK:!aECDH:!EDH-DSS-DES-CBC3-SHA:!EDH-RSA-DES-CBC3-SHA:!KRB5-DES-CBC3-SHA';
 ssl_prefer_server_ciphers on;

# Redirect POS to http
 location ~ ^/pos/web {
   rewrite ^(.*) http://$host:80$1 permanent;
 }

 # Redirect requests to odoo backend server
 location / {
   proxy_redirect off;
   proxy_pass http://odoo;
 }
 location /longpolling {
   proxy_redirect off;
   proxy_pass http://odoo_longpoll;
 }
}
```

# PostgreSQL configuration

Until now, we've used to deploy odoo and postgresql on the same server. We will now deploy PostgreSQL on his own server, and configure it.

![Odoo architecture layers](./img/oneservermultipleodoo.png )

## Use VM odoo-pg1

We will use a new VM and the private network.

Copy private/public ssh keys from odoo server, alter config, add hosts, ...

```
$ sudo vi /etc/ssh/sshd_config
```

```
AuthorizedKeysFile      %h/.ssh/authorized_keys
PubkeyAcceptedKeyTypes ssh-dss
```

```
$ sudo vi /etc/hosts
```

```
192.168.56.10   odoo-training
192.168.56.22   odoo-pg2
192.168.56.23   odoo-pg3
```

## Use apt.postgresql.org

Deploy it like in the single server scenario

```bash
$ wget https://anonscm.debian.org/cgit/pkg-postgresql/postgresql-common.git/plain/pgdg/apt.postgresql.org.sh
$ sudo bash apt.postgresql.org.sh
$ sudo apt-get install postgresql-9.6 postgresql-client-9.6 \
   postgresql-client-common postgresql-common \
   postgresql-server-dev-9.6 pg-activity
$ sudo su - postgres
```

We also need to set a password for the Odoo PostgreSQL user.

```
postgres> psql
postgres=# CREATE USER odoo WITH LOGIN CREATEDB PASSWORD 'OdooPostgrePWD';
postgres=# \q
postgres> exit
$
```

## Allow network connections

```
$ sudo vi /etc/postgresql/9.6/main/pg_hba.conf
```

```
...
# IPv4 local connections:
host    all             all             127.0.0.1/32            md5
host    all             all             192.168.56.0/24         md5
```

```
$ sudo vi /etc/postgresql/9.6/main/postgresql.conf
```

```
...
listen_addresses = '192.168.56.21'
```

```
$ sudo service postgresql restart
```

## STOP postgre on odoo

We need to stop and disable postgresql service on the odoo server, and connect odoo to our new postgresql server.

```bash
$ sudo systemctl stop postgresql
$ sudo systemctl disable postgresql
$ sudo vi /lib/systemd/system/odoo.service
```

```
...
After=network.target
```

```bash
$ sudo systemctl daemon-reload
$ sudo vi /etc/odoo/odoo10.conf
```

```
db_host = odoo-pg1
db_port = 5432
db_user = odoo
db_password = OdooPostgrePWD
```

## \# connections

This is very important to some of the below parameters (particularly work_mem) because there are some memory resources that are or can be allocated on a per-client basis, so the maximum number of clients suggests the maximum possible memory use

* set db_maxconn in odoo config
* ~4 connections per worker + 3 for admin

```bash
$ sudo vi /etc/postgresql/9.6/main/postgresql.conf
```

```
...
max_connections = 80
```

## shared_buffers

The shared_buffers configuration parameter determines how much memory is dedicated to PostgreSQL to use for caching data

* 25% of RAM on physical server
* recommended when in a VM: more than 55% VM RAM (VMWare doc)

```bash
$ sudo vi /etc/postgresql/9.6/main/postgresql.conf
```

```
...
shared_buffers = 1GB
```

You can retrieve the value the OS can allocate to PostgreSQL in monitoring systems like Munin

![Memory](./img/memory-day.png )

## effective_cache_size

effective_cache_size should be set to an estimate of how much memory is available for disk caching[...]

* Should be 50% of the RAM
* 75% of memory is a more aggressive but still reasonable amount

```
$ sudo vi /etc/postgresql/9.6/main/postgresql.conf
```

```
...
effective_cache_size = 1GB
```

## work_mem

If you do a lot of complex sorts, and have a lot of memory, then increasing the work_mem parameter allows PostgreSQL 
to do larger in-memory sorts which, unsurprisingly, will be faster than disk-based equivalents. This parameter is a 
per connection value!

```bash
$ sudo vi /etc/postgresql/9.6/main/postgresql.conf
```

```
...
work_mem = 64MB
```

## autovacuum

**Required to:**
* To recover or reuse disk space.
* To update data statistics used by the PostgreSQL query planner.
* To update the visibility map, which speeds up index-only scans.
* To protect against loss of very old data due to transaction ID wraparound or multixact ID wraparound.

**Should vacuum more than less**

## WAL size

Prior to 9.5, parameter was checkpoint_segments. It has been replaced in 9.5 with min_wal_size and max_wal_size

> max_wal_size = (3*checkpoint_segments) * 16MB

Note that the default setting for max_wal_size is much higher than the default checkpoint_segments used to be, 
so adjusting it might no longer be necessary.

## Good ideas only at first sight

Avoid to do this, you're probably not in a situation where it's required.

* **fsync = false** : Can cause data corruption
* **autovacuum = false** : Transaction ID Wraparound Failures
* **track_counts = false** : Needed by autovacuum

## What about file store?

We now have PostgreSQL datas stored on the DB server, we also need Filestore on the datas server

Even if NFS is not designed for performance, it's an easy way to achieve our goal, and due to the way Odoo handles 
files I/O, this will not be an issue.

## NFS server

On **odoo-pg1**, we deploy NFS server and allow connections from odoo servers.

```bash
$ sudo apt install nfs-kernel-server
$ sudo mkdir -p /export/odoo
$ sudo chown -R odoo /export
$ sudo vi /etc/exports
```

```
/export/odoo 192.168.56.0/255.255.255.0(rw,sync,no_subtree_check)
```

```
$ sudo exportfs -ra
$ sudo service nfs-kernel-server restart
```

## NFS client

On odoo-training, we deploy NFS client.

```bash
$ sudo apt install nfs-common
$ sudo mkdir /filestore
$ sudo chown -R odoo /filestore
$ sudo vi /etc/fstab
```

```
...
# Odoo filestore
odoo-pg1:/export/odoo /filestore nfs rw,hard,intr 0 0
```

```bash
$ sudo mount /filestore
$ cd ~/.local/share/Odoo
$ cp -R ./ /filestore/
$ sudo vi /etc/odoo/odoo10.conf
```

```
...
data_dir = /filestore
```

```bash
$ sudo service odoo restart
```

# Datas Replication

Rebuilding an Odoo server from scratch when all datas are stored on another server is quite fast and easy, 
rebuilding a data server (PostgreSQL and filestore) is a bit harder.

## Use VM odoo-pg2

We will use a new VM.

Copy private/public ssh keys from odoo server, alter config, add hosts, ...

```
$ sudo vi /etc/ssh/sshd_config
```

```
AuthorizedKeysFile      %h/.ssh/authorized_keys
PubkeyAcceptedKeyTypes ssh-dss
```

```bash
$ sudo vi /etc/hosts
```

```
192.168.56.10   odoo-training
192.168.56.21   odoo-pg1
192.168.56.23   odoo-pg3
```

## Use apt.postgresql.org

Deploy it like on odoo-pg1

```bash
$ wget https://anonscm.debian.org/cgit/pkg-postgresql/postgresql-common.git/plain/pgdg/apt.postgresql.org.sh
$ sudo bash apt.postgresql.org.sh
$ sudo apt-get install postgresql-9.6 postgresql-client-9.6 \
   postgresql-client-common postgresql-common \
   postgresql-server-dev-9.6 pg-activity
```

## Promote odoo-pg1

First, we'll promote odoo-pg1 as replication master.

```bash
$ python -c 'import base64, os; print(base64.b64encode(os.urandom(24)))'
$ sudo -u postgres psql -c "CREATE USER odoo_rep REPLICATION LOGIN
  PASSWORD 'ByrXga8IbnL5hNTeB46tj41e3B7edPs';"
$ sudo vi /etc/postgresql/9.6/main/postgresql.conf
```

```
...
wal_level = hot_standby
max_wal_senders = 3
wal_keep_segments = 8
archive_mode = on
full_page_writes = on
archive_command = 'cp "%p" "/var/lib/postgresql/9.6/shipped/%f"'
```

## Allow replication connections

```bash
$ sudo vi /etc/postgresql/9.6/main/pg_hba.conf
```

```
...
hostssl replication     odoo_rep      192.168.56.0/24          md5
```

```
$ sudo su - postgres
$ mkdir /var/lib/postgresql/9.6/shipped/
$ exit
```

## Initiate replication

It's now time to initiate replication from odoo-pg1 to odoo-pg2. We do the same config as on odoo-pg1, the main difference is the hot_standby parameter.

```bash
$ sudo vi /etc/postgresql/9.6/main/postgresql.conf
```

```
...
listen_addresses = '192.168.56.22'
max_connections = 80
shared_buffers = 1GB
effective_cache_size = 1GB
work_mem = 64MB
wal_level = hot_standby
max_wal_senders = 3
wal_keep_segments = 8
full_page_writes = on
archive_command = 'cp "%p" "/var/lib/postgresql/9.6/shipped/%f"'
hot_standby = on
```

## Allow connections

Even if not required, it's a good idea to permit connections to this slave the same way it is on the master. It will be easier in case of failover.

```
$ sudo vi /etc/postgresql/9.6/main/pg_hba.conf
```

```
...
# IPv4 local connections:
host    all             all           127.0.0.1/32            md5
host    all             all           192.168.56.0/24         md5
...
hostssl replication     odoo_rep      192.168.56.0/24         md5
```

## recovery.conf

We now configure odoo-pg2 To connect to odoo-pg1 to stream replicate.

```
$ sudo vi /etc/postgresql/9.6/main/recovery.conf
```

```
standby_mode = 'on'
primary_conninfo = 'host=odoo-pg1 port=5432 user=odoo_rep password=ByrXga8IbnL5hNTeB46tj41e3B7edPs sslmode=require'
trigger_file = '/tmp/postgresql.failover'
```

```
$ sudo su - postgres
$ mkdir /var/lib/postgresql/9.6/shipped/
$ exit
```

## Replication script

We will now destroy cluster on odoo-pg2 and dump the one from odoo-pg1 to start replication. 

**Keep care on what you're doing now, we destroy a db cluster!**

```bash
$ sudo vi ~/replicate.sh
```

```bash
echo Stopping PostgreSQL Slave node
sudo service postgresql stop

echo Drop old cluster
sudo -u postgres rm -rf /var/lib/postgresql/9.6/main

echo Performing base backup
sudo -u postgres pg_basebackup -h 192.168.56.21 -D /var/lib/postgresql/9.6/main -U odoo_rep -v -P
sudo -u postgres cp /etc/postgresql/9.6/main/recovery.conf /var/lib/postgresql/9.6/main/

echo Startging PostgreSQL Slave node
sudo service postgresql start
```

```
$ sudo chmod a+x ~/replicate.sh
$ ~/replicate.sh
```

## and Check that it's working!

```
$ sudo -u postgres psql -x -c "select * from pg_stat_replication;"
```

```
-[ RECORD 1 ]----+------------------------------
pid              | 8721
usesysid         | 24029
usename          | odoo_rep
application_name | walreceiver
client_addr      | 192.168.56.22
client_hostname  |
client_port      | 38268
backend_start    | 2016-09-01 17:01:38.184454+02
backend_xmin     |
state            | streaming
sent_location    | 0/23000060
write_location   | 0/23000060
flush_location   | 0/23000060
replay_location  | 0/23000000
sync_priority    | 0
sync_state       | async
```

## Replicate filestore

We will now replicate filestore to have a fully redundant data store. We'll use rsync, but other solutions based on clustered file systems, like drbd, are possible. On odoo-pg2:

```
$ sudo mkdir /export
$ sudo chown odoo /export
$ vi ~/syncfilestore.sh
```

```
#!/bin/bash
# Replicate odoo file store
rsync -az odoo@odoo-pg1:/export/ /export
```

```
$ crontab -e
```

```
*/5 * * * * /home/odoo/syncfilestore.sh
```

## Deploy odoo-pg3

As an exercice, deploy another slave postgresql server. Use odoo-pg3 VM for this purpose.

# Load balancing

Before adding more Odoo server to handle a higher load, we need something to distribute requests across the different odoo servers : **HAProxy**

![One Odoo on multiple servers](./img/oneodoomultipleserver.png )

## Deploy HAProxy VM

Deploy VM as usual :

* Network card
* /etc/hosts
* SSH
* Locale

```bash
$ sudo apt install haproxy
```

## SSL certificate

Use at least let's encrypt... Here we'll use a self signed as no public ip routing.

```bash
$ sudo mkdir /etc/ssl/odoo
$ sudo openssl genrsa -out /etc/ssl/odoo/odoo.key 1024
$ sudo openssl req -new -key /etc/ssl/odoo/odoo.key \
                   -out /etc/ssl/odoo/odoo.csr
> Country Name (2 letter code) [AU]:BE
> State or Province Name (full name) [Some-State]:Wal-Brabant
> Locality Name (eg, city) []:LLN
> Organization Name (eg, company) [Internet Widgits Pty Ltd]: PSTech
> Organizational Unit Name (eg, section) []:
> Common Name (e.g. server FQDN or YOUR name) []:odoo.training.internal
> Email Address []:

> Please enter the following 'extra' attributes to be sent with your certificate request
> A challenge password []:
> An optional company name []:
$ sudo openssl x509 -req -days 365 -in /etc/ssl/odoo/odoo.csr \
                    -signkey /etc/ssl/odoo/odoo.key \
                    -out /etc/ssl/odoo/odoo.crt
$ sudo cat /etc/ssl/odoo/odoo.crt /etc/ssl/odoo/odoo.key \
           | sudo tee /etc/haproxy/odoo.pem
```

## Configure HAProxy

```
$ sudo vi /etc/haproxy/haproxy.cfg
```

```
global
    log /dev/log    local1 warning
    stats socket /run/haproxy/admin.sock mode 660 level admin
    stats timeout 30s
    user haproxy
    group haproxy
    daemon
    maxconn 3000
    ca-base /etc/ssl/certs
    crt-base /etc/ssl/private
    ssl-default-bind-ciphers ECDH+AESGCM:DH+AESGCM:ECDH+AES256:DH+AES256:ECDH+AES128:DH+AES:ECDH+3DES:DH+3DES:RSA+AESGCM:RSA+AES:RSA+3DES:!aNULL:!MD5:!DSS
    ssl-default-bind-options no-sslv3 no-tls-tickets
    tune.ssl.default-dh-param 2048

defaults
    log global
    mode    http
    option  httplog
    option  dontlognull
        timeout connect 5000ms
        timeout client  900s
        timeout server  900s
        timeout check   90s

listen stats
    bind *:1936
    mode  http
    stats enable
    stats hide-version
    stats realm Haproxy\ Statistics
    stats auth odoo:odoo
    stats uri /haproxy-status
    
frontend odoo_no_ssl
    bind *:80
    maxconn 3000
    option http-server-close
    option forwardfor
    reqadd X-Forwarded-Proto:\ http
    reqadd X-Forwarded-Port:\ 80
    default_backend backend_odoo_no_ssl

frontend odoo_ssl
    bind *:443 ssl crt /etc/haproxy/odoo.pem
    maxconn 3000
    option http-server-close
    option forwardfor
    reqadd X-Forwarded-Proto:\ https
    reqadd X-Forwarded-Port:\ 443
    default_backend backend_odoo_ssl

backend backend_odoo_no_ssl
    mode http
    balance roundrobin
    option httpchk HEAD / HTTP/1.0\r\nHost:\ odoo.training.internal
    default-server inter 10s rise 1 fall 3
    http-check send-state
    server odoo1 192.168.56.10:80 check
    server odoo2 192.168.56.11:80 check

backend backend_odoo_ssl
    mode http
    balance roundrobin
    option httpchk HEAD / HTTP/1.0\r\nHost:\ odoo.training.internal
    default-server inter 10s rise 1 fall 3
    http-check send-state
    server odoo1 192.168.56.10:443 ssl verify none check check-ssl
    server odoo2 192.168.56.11:443 ssl verify none check check-ssl
```

### Test HAProxy

Change IP in your host file...

![One Odoo on multiple servers](./img/haproxy.png )

## Sessions cleaning

### Avoid having odoo itself cleaning sessions

Every ~1000 requests, Odoo list sessions, and remove the too old ones.
As it's not a problem on a local filesystem, this can be problematic on a shared filesystem, like the NFS one we're using.
To avoid this performance bottleneck, we'll stop to check this with Odoo itself, and use a linux cron to achieve this.

### Stop cleaning session in Python code

It's a bit tricky to change this behaviour. The method consist in a monkey patch of the method. Beware that this code
will reside in a module, and even if the module is not installed, due to the monkey patch nature of the module, the code
will be executed.

in session.py:

```python
from openerp import http

def session_gc(session_store):
    pass
    
http.session_gc = session_gc
```

in __init__.py:

```python
import session
```

### Creating the session cleaning cron

```bash
$ crontab -e
```

```
48 * * * * find /filestore/sessions -mtime +8 -delete
```

## Improve admissible load

Simply duplicate odoo server, change ip and hostname...

* clone VM in virtualbox
* sudo vi /etc/hostname
* sudo vi /etc/hosts
* sudo vi /etc/network/interfaces

That's it, you've a new server able to respond to odoo queries.

As an exercice, deploy an odoo-3 vm and add it to the haproxy pool

## Update source on a HA cluster

Some process, like the bundle generation, rely on the last modified date of the files contained in the bundle.
If those dates are different on the two servers, the bundle will be re-generated continously, and you'll face 404 errors.

To ensure a proper bundle generation, all dates must be identical between the servers. To achive this, can have two 
solutions:

* A share drive
* A rsync between the servers

As we already have deployed a share drive for filestore, it's easy to achive this for code. 

We'll explain here the rsync method

### Sync code base

To update source code on servers, we will do a **git checkout** on one server, or a **git pull**, and sync the code 
on the other ones.

On server **odoo-1**:

```bash
$ cd /opt/odoo10/odoo
$ git pull
$ cd /opt/odoo10/enterprise
$ git pull
[...]
$ cd /opt/odoo10/my_modules
$ git pull
[...]
```

On server **odoo-2** (and odoo-3, odoo-xxx, ...):

```bash
$ rsync -az odoo@odoo-1:/opt/odoo10/ /opt/odoo10
```

# Etherpad

## node.js

```bash
$ sudo apt install -y build-essential
$ cd
$ curl -sL https://deb.nodesource.com/setup_4.x | sudo -E bash -
$ sudo apt-get install -y nodejs
```

## Etherpad

```bash
$ sudo apt install libssl-dev pkg-config
$ cd /opt
$ sudo mkdir etherpad
$ sudo mkdir /var/log/etherpad
$ sudo chown odoo etherpad
$ sudo chgrp odoo etherpad
$ cd etherpad
$ git clone git://github.com/ether/etherpad-lite.git
$ sudo adduser etherpad --system --group --home /var/etherpad
$ sudo chown -R etherpad /var/log/etherpad
$ sudo chown -R etherpad etherpad-lite
$ cd etherpad-lite
$ ./bin/run.sh
```

```
$ sudo vi /opt/etherpad/etherpad-lite/settings.json
```

```
"trustProxy" : true,
"users": {
    "admin": {
      "password": "admin",
      "is_admin": true
    },
    "user": {
      "password": "user",
      "is_admin": false
    }
},
  "defaultPadText" : "",
  "suppressErrorsInPadText" : true,
"logconfig" :
    { "appenders": [
        /*{ "type": "console"
        //, "category": "access"// only logs pad access
        }*/
      { "type": "file"
      , "filename": "/var/log/etherpad/etherpad.log"
      , "maxLogSize": 1024
      , "backups": 3 // how many log files there're gonna be at max
      //, "category": "test" // only log a specific category
        }
```

```
$ sudo vi /lib/systemd/system/etherpad.service
```

```
[Unit]
Description=Etherpad-lite, the collaborative editor.
After=syslog.target network.target

[Service]
Type=simple
User=etherpad
Group=etherpad
WorkingDirectory=/opt/etherpad/etherpad-lite
ExecStart=/opt/etherpad/etherpad-lite/bin/run.sh
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
$ sudo chown -R etherpad /opt/etherpad/etherpad-lite
$ sudo systemctl daemon-reload
$ sudo systemctl start etherpad
$ sudo systemctl enable etherpad
```

If etherpad doesn't start, check with

```bash
$ journalctl
```

## Proxiing etherpad

```bash
$ sudo vi /etc/nginx/sites-available/pad
```

```
server {
    listen 80;
    server_name pad.training.internal;

    #log
    access_log /var/log/nginx/etherpad.access.log;
    error_log /var/log/nginx/etherpad.error.log;

    # Redirect requests to etherpad backend server
    location / {
      proxy_redirect off;
      proxy_set_header Host $host;
      proxy_pass http://127.0.0.1:9001;
    }
}
```

```bash
$ sudo ln -s /etc/nginx/sites-available/pad /etc/nginx/sites-enabled/pad
$ sudo service nginx restart
```

## Test it

Install module **Pad on tasks**

```
$ cat /opt/etherpad/etherpad-lite/APIKEY.txt
```

* Settings->General settings->Configure your company data
* In configuration tab:

* pad server = http://pad.training.internal
* Pad Api Key = content of APIKEY.txt

### If etherpad is stopped

Test by stopping it
![No pad server](./img/lostpad.png )

### If description is empty

If task description is empty after filling it within the pad, that's because odoo server cannot contact pad server

check name resolution on the odoo server. In this training, edit /etc/hosts on the odoo server

```
127.0.0.1	localhost pad.training.internal
127.0.1.1	odoo-training

# The following lines are desirable for IPv6 capable hosts
::1     localhost ip6-localhost ip6-loopback
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
```

# Backup

## PostgreSQL

You've mainly 2 ways to do backups:

* pg_dump
* pg_basebackup

Each one have pros and cons. There's no one size fits all solution, mainly dependant on :

* RTO: Recovery Time Objective
* RPO: Recovery Point Objective

![No pad server](./img/rtorpo.jpg )

### pg_dump

The most used solution, permit to backup and restore databases one at a time.

```
$ pg_dump -Fc -d odoo > odoo.backup
```

```
$ pg_restore -d odoo -j8 odoo.backup
```

Can also use text format, easy to migrate from one postgresql version to another (>=)

```
$ pg_dump -d odoo > odoo.backup
```

```
$ psql -d odoo < odoo.backup
```

Can also be used to copy to a test server

```
$ pg_dump -Fc -d odoo | pg_restore -d odoo -h my_other_server
```

### pg_basebackup

Backup the whole database cluster. Already used in training for starting streaming replication. Can be used to backup a database, and restore it with WAL files to minimise RPO.

```
$ pg_basebackup --xlog --format=t -D /backups/`date +%Y%m%d`
```

This create a tar with the whole database storage. To restore, simply stop the cluster, remove the file system directory and replace with the backup content.

To incluide WAL files, create a recovery.conf file in the cluster data directory, containing:

```
restore_command = 'cp /mnt/server/archivedir/%f %p'
```

Adapt the command to your configuration. If you choose this backup/restore method, train yourself to be ready!

# Monitor

Munin require 1 master server which collects datas, and plenty of node where to collect datas from. We will use a new VM for the main munin server.

Copy private/public ssh keys from odoo server, alter config, add hosts, ...

```
$ sudo vi /etc/ssh/sshd_config
```

```
AuthorizedKeysFile      %h/.ssh/authorized_keys
PubkeyAcceptedKeyTypes ssh-dss
```

```
$ sudo vi /etc/hosts
```

```
192.168.56.10  odoo-1
192.168.56.11  odoo-2
192.168.56.12  odoo-3
192.168.56.21  odoo-pg1
192.168.56.22  odoo-pg2
192.168.56.23  odoo-pg3
192.168.56.30  haodoo
```

## Install Munin package

```
$ sudo apt install munin
```

This will install munin, as well as munin-node (for local server monitoring), some plugins, ...

We need only one Munin, but we'll need to deploy munin-node on each node to monitor.

## Install NGinx

We'll use NGinx to serve static files generated by munin. It's also possible to use NGinx as a proxy to forward requests to munin-http.

```
$ sudo apt install nginx apache2-utils
$ sudo htpasswd -cb /etc/nginx/htpasswd admin admin
$ sudo vi /etc/nginx/sites-enabled/default
```

```
server {
    listen 80 default_server;
    listen [::]:80 default_server;

    location / {
        rewrite ^/$ munin/ redirect; break;
    }
    location /munin/static/ {
        alias /etc/munin/static/;
        expires modified +1w;
    }
    location /munin/ {
        auth_basic            "Restricted";
        # Create the htpasswd file with the htpasswd tool.
        auth_basic_user_file  /etc/nginx/htpasswd;

        alias /var/cache/munin/www/;
        expires modified +310s;
    }
}
```

Munin is up and running, and published in http.

## Monitor a first node

As a first node, we'll use our HaProxy server. We'll deploy on it standard monitoring as well as more specific ones.

```
$ sudo apt install munin-node
```

Allow munin server to monitor this node

```
$ sudo vi /etc/munin/munin-node.conf
```

```
...
host_name haodoo
allow ^192\.168\.56\.40$
...
```

Add this node in server configuration

```
$ sudo vi /etc/munin/munin.conf
```

```
...
[ha;haodoo]
    address 192.168.56.30
...
```

Munin is able to monitor pretty anything. The node has for job to measure and send datas to master. By default, some plugins are already deployed (ram, cpu, ...) but we can add somes more relevant to our system. A way to determine which plugins are usefull is to use munin-node-configure itself :

```
$ sudo munin-node-configure --suggest
```

```
Plugin                     | Used | Suggestions
------                     | ---- | -----------
acpi                       | no   | no [cannot read /proc/acpi/thermal_zone/*/temperature]
amavis                     | no   | no
apache_accesses            | no   | no [LWP::UserAgent not found]
apache_processes           | no   | no [LWP::UserAgent not found]
apache_volume              | no   | no [LWP::UserAgent not found]
apc_envunit_               | no   | no [no units to monitor]
bonding_err_               | no   | no [No /proc/net/bonding]
courier_mta_mailqueue      | no   | no [spooldir not found]
courier_mta_mailstats      | no   | no [could not find executable]
courier_mta_mailvolume     | no   | no [could not find executable]
cps_                       | no   | no
cpu                        | yes  | yes
...
```

Result show what's installed and what should be.

It's possible to add more plugins on node :

```
$ sudo apt install libwww-perl
$ ls /usr/share/munin/plugins/ha*
/usr/share/munin/plugins/haproxy_  /usr/share/munin/plugins/haproxy_ng
```

Those 2 plugins seems relevant to our particular node. Let's deploy them

```
$ sudo ln -s /usr/share/munin/plugins/haproxy_ /etc/munin/plugins/haproxy_backend
$ sudo ln -s /usr/share/munin/plugins/haproxy_ng /etc/munin/plugins/haproxy_ng
$ sudo vi /etc/munin/plugin-conf.d/munin-node
```

```
...
[haproxy_*]
env.url http://odoo:odoo@localhost:1936/haproxy-status?stats;csv
```

```
$ sudo service munin-node restart
```

## Define alarm threshold

Monitoring is good, and is even better if I can define my own threshold for warning and critical level. Thoses levels can be defined on the node, in the plugin configuration if plugin handle it. Or can be defined on the server. In the case of the haproxy_ng plugin, it doesn't handle warning and critical levels. So, on the munin server, not the node:

```
$ sudo vi /etc/munin/munin.conf
```

```
[ha;haodoo]
    address 192.168.56.30
    HAPActive.backend_odoo_ssl_act.warning 2:
    HAPActive.backend_odoo_ssl_act.critical 1:
    HAPActive.backend_odoo_no_ssl_act.warning 2:
    HAPActive.backend_odoo_no_ssl_act.critical 1:
```
![Munin alarm](./img/critical.png )

It's also possible to add more plugins on node, from github for example, like the ones from https://github.com/munin-monitoring/contrib

```bash
$ sudo rm /etc/munin/plugins/haproxy_ng
$ cd /opt
$ sudo git clone https://github.com/munin-monitoring/contrib.git
$ sudo ln -s /opt/contrib/plugins/haproxy/haproxy_active_backend /etc/munin/plugins/haproxy_active_backend
$ sudo ln -s /opt/contrib/plugins/haproxy/haproxy_abort_backend /etc/munin/plugins/haproxy_abort_backend
$ sudo vi /etc/munin/plugin-conf.d/munin-node
```

```
[haproxy_*]
env.url http://odoo:odoo@localhost:1936/haproxy-status?stats;csv
env.backend backend_odoo_no_ssl backend_odoo_ssl
```

```bash
$ sudo service munin-node restart
```

## Monitor PostgreSQL

As datas resides on this server, it's important to monitor this particular server. Depending on your configuration, some metrics are relevant or not, like replication delay. We add postgresql server 1 in munin config then check plugins on the postgresql node.

Allow munin server to monitor this node

```bash
$ sudo apt install munin-node libdbd-pg-perl
$ sudo vi /etc/munin/munin-node.conf
```

```
...
host_name odoo-pg1
allow ^192\.168\.56\.40$
...
```

Configure munin server to monitor it

```bash
$ sudo vi /etc/munin/munin.conf
```

```
[pg;odoo-pg1]
    address 192.168.56.21
[pg;odoo-pg2]
    address 192.168.56.22
```

### Suggest PostgreSQL plugins

```
$ sudo munin-node-configure --suggest
```

```
...
postgres_autovacuum        | no   | yes
postgres_bgwriter          | no   | yes
postgres_cache_            | no   | yes (+ALL +odoo)
postgres_checkpoints       | no   | yes
postgres_connections_      | no   | yes (+ALL +odoo)
postgres_connections_db    | no   | yes
postgres_locks_            | no   | yes (+ALL +odoo)
postgres_oldest_prepared_xact_ | no   | no [Prepared transactions not enabled]
postgres_prepared_xacts_   | no   | no [Prepared transactions not enabled]
postgres_querylength_      | no   | yes (+ALL +odoo)
postgres_scans_            | no   | yes (+odoo)
postgres_size_             | no   | yes (+ALL +odoo)
...
```

As suggested, deploy the PostgreSQL plugins

```
$ sudo munin-node-configure --shell
ln -s '/usr/share/munin/plugins/postgres_autovacuum' '/etc/munin/plugins/postgres_autovacuum'
ln -s '/usr/share/munin/plugins/postgres_bgwriter' '/etc/munin/plugins/postgres_bgwriter'
ln -s '/usr/share/munin/plugins/postgres_cache_' '/etc/munin/plugins/postgres_cache_ALL'
ln -s '/usr/share/munin/plugins/postgres_cache_' '/etc/munin/plugins/postgres_cache_odoo'
ln -s '/usr/share/munin/plugins/postgres_checkpoints' '/etc/munin/plugins/postgres_checkpoints'
ln -s '/usr/share/munin/plugins/postgres_connections_' '/etc/munin/plugins/postgres_connections_ALL'
ln -s '/usr/share/munin/plugins/postgres_connections_' '/etc/munin/plugins/postgres_connections_odoo'
ln -s '/usr/share/munin/plugins/postgres_connections_db' '/etc/munin/plugins/postgres_connections_db'
ln -s '/usr/share/munin/plugins/postgres_locks_' '/etc/munin/plugins/postgres_locks_ALL'
ln -s '/usr/share/munin/plugins/postgres_locks_' '/etc/munin/plugins/postgres_locks_odoo'
ln -s '/usr/share/munin/plugins/postgres_querylength_' '/etc/munin/plugins/postgres_querylength_ALL'
ln -s '/usr/share/munin/plugins/postgres_querylength_' '/etc/munin/plugins/postgres_querylength_odoo'
ln -s '/usr/share/munin/plugins/postgres_scans_' '/etc/munin/plugins/postgres_scans_odoo'
ln -s '/usr/share/munin/plugins/postgres_size_' '/etc/munin/plugins/postgres_size_ALL'
ln -s '/usr/share/munin/plugins/postgres_size_' '/etc/munin/plugins/postgres_size_odoo'
ln -s '/usr/share/munin/plugins/postgres_transactions_' '/etc/munin/plugins/postgres_transactions_ALL'
ln -s '/usr/share/munin/plugins/postgres_transactions_' '/etc/munin/plugins/postgres_transactions_odoo'
ln -s '/usr/share/munin/plugins/postgres_tuples_' '/etc/munin/plugins/postgres_tuples_odoo'
ln -s '/usr/share/munin/plugins/postgres_users' '/etc/munin/plugins/postgres_users'
ln -s '/usr/share/munin/plugins/postgres_xlog' '/etc/munin/plugins/postgres_xlog'
$ sudo munin-node-configure --shell | sudo sh
$ sudo service munin-node restart
```

### Monitor replication

All thoses plugins are cool, but I want to monitor my streaming replication!

```
$ sudo vi /etc/munin/plugins/pg_replication
```

```
#!/usr/bin/env bash
#%# family=manual

slave=`psql postgres -A -t -c "SELECT pg_is_in_recovery();"`
master=`psql postgres -A -t -c "SELECT count(client_addr) from pg_stat_replication;"`

if [[ $slave == "f" ]];
then
    if [[ $master -eq 0 ]];
    then
        exit 1
    else
        client=`psql postgres -A -t -c "SELECT client_addr from pg_stat_replication;"`
        client=`dig -x $client +short`
    fi
fi

case $1 in
    config)
        echo graph_category postgres
        echo graph_title Streaming Replication
        if [[ $master -gt 0 ]]; then
            echo delay_b.label Replication Lag \($client\)\(B\)
            echo delay_b.warning   10000000
            echo delay_b.critical 300000000
        fi
        if [[ $slave == "t" ]]; then
            echo graph_args --logarithmic --units=si
            echo delay_s.label Replication Delay \(s\)
            echo delay_s.warning   60
            echo delay_s.critical 600
            echo delay_b.label Replication Lag \(B\)
            echo delay_b.warning   10000000
            echo delay_b.critical 300000000
        fi
        exit 0
        ;;
esac

if [[ $master -gt 0 ]]; then
    # master
    echo -n "delay_b.value "
    psql postgres -A -t -c "select pg_xlog_location_diff(sent_location, replay_location) from pg_stat_replication;"
fi

if [[ $slave == "t" ]]; then
    # slave
    echo -n "delay_s.value "
    psql postgres -A -t -c "
    SELECT
    CASE
        WHEN pg_last_xlog_receive_location() = pg_last_xlog_replay_location() THEN 0
        ELSE EXTRACT (EPOCH FROM now() - pg_last_xact_replay_timestamp())
    END;"
    echo -n "delay_b.value "
    psql postgres -A -t -c "SELECT pg_xlog_location_diff(pg_last_xlog_receive_location(), pg_last_xlog_replay_location());"
fi

exit 0
```

```
$ sudo chmod a+x /etc/munin/plugins/pg_replication
$ sudo vi /etc/munin/plugin-conf.d/munin-node
```

```
[pg_*]
user postgres
group postgres
```

Don't forget ot restart munin-node on the node, and you can run munin-cron on the master as munin user to speed up a bit. 
You can also run munin-run pg_replication on the node to check if everything is ok.

![Munin alarm](./img/pg_replication.png )

## Other usefull graphs

Some graphs are activated by default, and used to diagnose performance issues, size postgresql memory, ...

* Disk IOs
* Disk latency
* CPU Usage (iowait, steal, ...)
* Load average
* Memory usage (cache, ...)

## Monitor Odoo node

As usual, deploy munin-node on your server and ask munin main server to monitor it.

```
$ sudo apt install munin-node
$ sudo vi /etc/munin/munin-node.conf
```

```
...
host_name odoo-1
allow ^192\.168\.56\.40$
...
```

Configure munin server to monitor it

```
$ sudo vi /etc/munin/munin.conf
```

```
[odoo;odoo-1]
    address 192.168.56.10
[odoo;odoo-2]
    address 192.168.56.11
```

### Adjust log-level

We want to monitor response time within odoo. To achieve this, we need to get the response time from odoo, in the odoo logs. In your odoo config file:

```
log_level = debug_rpc
```

This will generate logs like:

```
2016-09-22 12:23:11,205 30977 DEBUG 9dpm-test openerp.http.rpc.request: read_subscription_data: None 
    None: time:0.014s mem: 1005056k -> 1005056k (diff: 0k)
2016-09-22 12:23:11,206 30977 INFO 9dpm-test werkzeug: 127.0.0.1 - - [22/Sep/2016 12:23:11] "POST
    /mail/read_subscription_data HTTP/1.1" 200 -
2016-09-22 12:23:11,485 30977 DEBUG 9dpm-test openerp.http.rpc.request: call_kw: order.category r
    ead: time:0.235s mem: 1005056k -> 1006080k (diff: 1024k)
2016-09-22 12:23:11,486 30977 INFO 9dpm-test werkzeug: 127.0.0.1 - - [22/Sep/2016 12:23:11] "POST
    /web/dataset/call_kw/order.category/read HTTP/1.1" 200 -
2016-09-22 12:23:11,750 30977 DEBUG 9dpm-test openerp.http.rpc.request: call_kw: sale.order.line 
    read: time:0.152s mem: 1006080k -> 1007360k (diff: 1280k)
2016-09-22 12:23:11,752 30977 INFO 9dpm-test werkzeug: 127.0.0.1 - - [22/Sep/2016 12:23:11] "POST
    /web/dataset/call_kw/sale.order.line/read HTTP/1.1" 200 -
2016-09-22 12:23:12,074 30977 DEBUG 9dpm-test openerp.http.rpc.request: call_kw: sale.order.line 
    read: time:0.169s mem: 1007360k -> 1008128k (diff: 768k)
2016-09-22 12:23:12,075 30977 INFO 9dpm-test werkzeug: 127.0.0.1 - - [22/Sep/2016 12:23:12] "POST
    /web/dataset/call_kw/sale.order.line/read HTTP/1.1" 200 -
```

### How many users?

A usual question is "how many concurrent users do I have?", and another one is "How many transactions/minute do they do?". As the number of workers and thus CPU is directly linked to this answer, it's important to answer.

We can distinguish two kind of requests. The longpoll ones, and the others.

Number of longpoll requests per minute ~= number of users, even inactive with just an open browser tab.

Other requests are sent by active users.

```bash
$ sudo vi /etc/munin/plugins/odootrmin
```

```bash
#!/bin/sh
#%# family=manual
#%# capabilities=autoconf suggest
case $1 in
  autoconf)
      exit 0
      ;;
  suggest)
      exit 0
      ;;
  config)
      echo graph_category odoo
      echo graph_title odoo rpc request count
      echo graph_vlabel num requests/minute in last 5 minutes
      echo requests.label num requests
      echo pollrequests.label num poll requests
      exit 0
      ;;
esac
# watch out for the time zone of the logs => using date -u for UTC timestamps
result=$(tail -60000 /var/log/odoo/odoo.log | grep -a "odoo.http.rpc.request" | grep -a -v "poll" | awk "BEGIN{count=0} (\$1 \" \" \$2) >= \"`date +'%F %H:%M:%S' -ud '5 min ago'`\" { count+=1; } END{print count/5}")
pollresult=$(tail -60000 /var/log/odoo/odoo.log | grep -a "odoo.http.rpc.request" | grep -a "poll" | awk "BEGIN{count=0} (\$1 \" \" \$2) >= \"`date +'%F %H:%M:%S' -ud '5 min ago'`\" { count+=1; } END{print count/5}")
echo "requests.value ${result}"
echo "pollrequests.value ${pollresult}"
exit 0
```

Once munin node restarted, and munin cron ran, a new graph appears.

![Munin alarm](./img/odootrmin.png )

### Measure response time

It's possible to extract the rpc response time from odoo logs. in /etc/munin/plugins/odooresponse:

```bash
#!/bin/sh
#%# family=manual
#%# capabilities=autoconf suggest
case $1 in
config)
echo graph_category odoo
echo graph_title odoo rpc requests min/average response time
echo graph_vlabel seconds
echo graph_args --units-exponent -3
echo min.label min
echo min.warning 1
echo min.critical 5
echo avg.label average
echo avg.warning 1
echo avg.critical 5
exit 0
;;
esac
# watch out for the time zone of the logs => using date -u for UTC timestamps
result=$(tail -60000 /var/log/odoo/odoo.log | grep -a "odoo.http.rpc.request" | grep -a -v "poll" | awk "BEGIN{sum=0;count=0} (\$1 \" \" \$2) >= \"`date +'%F %H:%M:%S' -ud '5 min ago'`\" {split(\$8,t,\":\");time=0+t[2];if (min==\"\") { min=time}; sum += time; count+=1; min=(time>min)?min:time } END{print min, sum/count}")
echo -n "min.value "
echo ${result} | cut -d" " -f1
echo -n "avg.value "
echo ${result} | cut -d" " -f2
exit 0
```

Once munin node restarted, and munin cron ran, a new graph appears.

![Munin alarm](./img/responsetime.png )
