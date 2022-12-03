# ip_change_logger
This python-script is meant to log changes of the public ip-address and signal the change via E-Mail or other ways.

It was developed so it can easily be run on a server (e. g. via crontab). It is important to know, that there is no
constant logging. Logging only takes place when the script is executed. There is no logging in the background or
anything like that.

## Important files

### main.py
The place of the main program loop. If you want to use the program that is the file you need to execute. At the top of
the file there are several things you can adjust. For future releases, this will be kept seperate in a config-file or
something like that.

### f_getip.py
Different functions are defined in this file for getting the public ip-address. As this is the heart of the program (it
is meant to track the public ip-address, right?) I implemented different ways of getting the public ip-address so there
should always be a solution that fits your needs. You can define which one to use at the top of the main.py file.

### f_signal.py
Different functions are defined in this file for signaling the change of the public ip-address. Currently there is only
one function (E-Mail via SendGrid) but further development is on the way. You can define if the script should signal
you at the top of the main.py file.

### data.json
In this file is currently tracked the last time a change of the public ip-address is recognized. It is planned to
change this in future releases and record all results every time the script runs. The file is created when the program
runs for the first time.

### .env
At several points the storing of credentials is sometimes unavoidable. Credentials like API keys will be stored in
environment variables. For easier handling they could also be stored in an .env file. This is not recommended for
production use.

At the moment the following environment variable are in use:
- SENDGRID_API_KEY -> E-Mail signaling via SendGrid

### LICENSE
GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007

## Version
V 1.0.0