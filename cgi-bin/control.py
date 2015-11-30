#!/usr/bin/env python

import fcntl
import os
import cgi
import Cookie
import errno

import numpy

parent = os.getcwd()
max_users=20

arguments = cgi.FieldStorage()

cmd = arguments['cmd'].value

thiscookie = Cookie.SimpleCookie()

user_agent = os.environ["HTTP_USER_AGENT"]
user_ip = os.environ["REMOTE_ADDR"]
                
# reads the cookie
if os.environ.has_key('HTTP_COOKIE'):
    thiscookie.load(os.environ['HTTP_COOKIE'])
    if 'name' not in thiscookie.keys(): # new user
        print "Content-type: text/html\n\n"
        print "<h1>Your are not registered or your browser does not accept cookies...</h1>"
    else:
        max_users = 20
        
        users_filename = parent+"/data/users_details.dat"
        users_details = numpy.memmap(users_filename, dtype="S120", mode='r', shape=(max_users,3)) # overwrites any existent file

        users_filename = "data/users_cmds.dat"
        users_cmds = numpy.memmap(users_filename, dtype=numpy.int32, mode='r+', shape=(max_users,3)) # overwrites any existent file        
        
                
        search_ip = numpy.where(users_details[:,2]==user_ip)[0]
        
        user_idx = search_ip[0]
        
        if cmd=="up":
            users_cmds[user_idx,1]+=1
            
        if cmd=="down":
            users_cmds[user_idx,1]-=1
            
        if cmd=="left":
            users_cmds[user_idx,0]+=1
            
        if cmd=="right":
            users_cmds[user_idx,0]-=1

        if cmd=="fire":
            users_cmds[user_idx,2]=1
            
        print "Content-type: text/html\n\n"