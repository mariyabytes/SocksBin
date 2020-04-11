SocksBin
=====

Command line pastebin for sharing files and command outputs.

# How to use

### Requirements
To use this, you'll need a tool called **netcat**. Try typing 'nc' or 'netcat' into the terminal, you probably have it already !

_________
### Client Side

* Self-Explanatory examples using the public server


```
echo "Hello World !" | nc magnum.wtf 6969
```

```
cat "script.sh" | nc magnum.wtf 6969
```

* In case you started the server on localhost


```
df | nc localhost 9999
```

____

You will receive a url to the text-only paste as a response to the above commands. e.g.

```
https://socksbin.magnum.wtf/33fdd867
```

This has a built-in Pygment-based beautifier. add "_color" to the end of the received url, to get a beautified paste.

```
https://socksbin.magnum.wtf/33fdd867_color
```

<sup>In case your text isn't beautified, include the *shebang* `#!` which is the first two bytes of an executable</sup>

<sup> e.g. the first line should be `#! /usr/bin/env python` for proper python formatting</sup>

-------------------------------------------------------------------------------

## Cool stuff

Make this much easier to use by adding an alias to your rc file. For example:

-------------------------------------------------------------------------------

### `skb` alias

__Linux (Bash):__

```
echo 'alias skb="nc magnum.wtf 6969"' >> .bashrc
```


__macOS:__

```
echo 'alias skb="nc magnum.wtf 9999"' >> .bash_profile
```

-------------------------------------------------------------------------------

### Copy output to clipboard

__Linux (Bash):__
```
echo 'alias skb="netcat magnum.wtf 6969 | xclip -selection c"' >> .bashrc
```

```
echo less typing now! | skb
```

__macOS:__

```
echo 'alias skb="nc magnum.wtf 6969 | pbcopy"' >> .bash_profile
```

```
echo less typing now! | skb
```

__Remember__ to reload the shell with `source ~/.bashrc` or `source ~/.bash_profile` after adding any of provided above!

-------------------------------------------------------------------------------


# Server Side 

## Configration

* Clone

```
git clone https://github.com/MagnumDingusEdu/SocksBin.git
```

* Set up virtual environment

```
python3 -m venv venv

# or 

virtualenv venv
```

* Install required packages

```
source venv/bin/activate
pip intall -r requirements.txt
```

* Make the script executable

```
chmod +x paster.py
```

_____________________________________________

# Usage

```
usage: ./paster.py [-o output directory]
                   [-n listen_address] [-p port] [-s slug size]
                   [-l logfile] [-b buffer size][-h help]
```

These are command line arguments. None of these are required to run the server. Defaults are specified in the section below.

_____________________________________________


### Settings

-------------------------------------------------------------------------------

#### Output directory `-o` `--output_directory`

Absolute, or relative path to the directory where the pastes will be stored, as plaintext files.

```
./paster.py -o ./pastes
```

```
./paster.py -o /home/www/pastes/
```

__Default value:__ `$HOME/socksbin`

-------------------------------------------------------------------------------

#### URL `-u` `--url`

This will be used as a prefix for an url received by the client.
Value will be prepended with `$url`.

```
./paster.py -u https://domain.com/
```

```
./paster.py -u https://subdomain.domain.com/
```

```
./paster.py -u https://subdomain.domain.com/pastes/
```

__Default value:__ `http://localhost/`

-------------------------------------------------------------------------------

#### Slug size `-s` `--slug_size`

This will force slugs to be of required length:

```
./paster.py -s 6
```

__Output url with default value__: `http://localhost/********`,
where * is a randomized character

__Output url with example value 6__: `http://localhost/******`,
where * is a randomized character

__Default value:__ 8


-------------------------------------------------------------------------------

#### Buffer size `-b` `--buffer_size`

This parameter defines size of the buffer in bytes, when making a connection.
TCP has a max buffer size of 60K.
```
./paster.py -b 4096
```

__Default value:__ 32768

-------------------------------------------------------------------------------

#### Log file `-l` `--log_file`

```
./paster.py -l /home/user/socksbin.log.txt
```

The log file will only be made if you specify this argument. Make sure that this file is user writable.

__Default value:__ not set


-------------------------------------------------------------------------------

#### Queue Depth `-q` `--queue_depth`

```
./paster.py -q 10
```

The helps to properly manage simultaneous connections. The maximum value is system dependent. For example, on Linux, see /proc/sys/net/core/somaxconn

__Default value:__ 10

------------------------------------------------------------------------------

### Running as a service

If you're using systemd, follow these steps:

* Create the service file

```
sudo touch /lib/systemd/system/socksbin.service
```

* Add the following code to the file

```
[Unit]
Description=Socksbin Server
After=multi-user.target

[Service]
Type=idle
ExecStart=/home/user/socksbin/venv/bin/python /home/user/socksbin/paster.py -o /var/www/socksbin -s 8 -p 6969 -l /home/phallus/socklog.txt -u https://subdomain.yourdomain.com/

[Install]
WantedBy=multi-user.target
```

Replace */home/user/socksbin* with the path to your socksbin installation. Save and exit.

* Set appropriate permissions

```
sudo chmod 644 /lib/systemd/system/socksbin.service
```

* Restart the systemd daemon, and enable your service

```
sudo systemctl daemon-reload
sudo systemctl start socksbin
sudo systemctl enable socksbin
```

This will make sure it remains up even accross reboots.

To check the current status of your service:

```
sudo systemctl status socksbin
```

---------------------------------------------------------------------



## Example Server Configs

This does not have a web server built in, so you can use this with your existing web server, to make files available to the internet.

* Example apache config

```
<VirtualHost *:80>
        ServerName subdomain.mysite.com
        ServerAdmin webmaster@localhost
        DocumentRoot /var/www/socksbin
        DirectoryIndex index.html

        ErrorLog ${APACHE_LOG_DIR}/socksbin_error.log
        CustomLog ${APACHE_LOG_DIR}/socksbin_access.log combined

</VirtualHost>
```

* Example nginx config


```
server {
    listen 80;
    server_name subdomain.mysite.com;
    charset utf-8;

    location / {
            root /var/www/socksbin/;
            index index.txt index.html;
    }
}
```

**Please make sure that you put default file, e.g. index.html, so that people can't access all your files freely.**

__________________________________________________________________

I'm new at this, any changes will be absolutely welcome. Thank you for reading this !



