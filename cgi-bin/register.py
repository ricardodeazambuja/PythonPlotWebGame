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

if 'name' in arguments.keys():
    
    user_name = arguments['name'].value
    
    thiscookie = Cookie.SimpleCookie()

    user_agent = os.environ["HTTP_USER_AGENT"]
    user_ip = os.environ["REMOTE_ADDR"]

    # reads the cookie
    if os.environ.has_key('HTTP_COOKIE'):
        thiscookie.load(os.environ['HTTP_COOKIE'])
        if 'name' not in thiscookie.keys(): # new user
            thiscookie['name'] = user_name
            thiscookie['name']['max-age'] = 24*60
            # thiscookie['user_name']['path'] = 'cgi-bin/'
        else:
            thiscookie['name'] = user_name
            thiscookie['name']['max-age'] = 24*60
            # thiscookie['user_name']['path'] = 'cgi-bin/'        

        with open(parent+'/data/lockfile.dat','r+') as f:

            # Traps the script here until it gets the lock
            while True:
                try:
                    # Tries to get the lock
                    fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)

                    total_number = int(f.readline())
                    break
                except IOError as ex:
                    # raise on unrelated IOErrors
                    if ex.errno != errno.EAGAIN:
                        raise
                else:
                    time.sleep(0.1)

            users_filename = parent+"/data/users_details.dat"
            users_details = numpy.memmap(users_filename, dtype="S120", mode='r+', shape=(max_users,3)) # overwrites any existent file

            search_ip = numpy.where(users_details[:,2]==user_ip)[0]

            if search_ip.size>0:
                user_idx = search_ip[0]
            else:
                # Adds one more user if it's new
                total_number+=1
                f.seek(0)
                f.write(str(total_number)+'\n')
                user_idx = total_number-1

            users_details[user_idx,0]=user_name
            users_details[user_idx,1]=user_agent
            users_details[user_idx,2]=user_ip
            users_details.flush()


            # Releases the lock at the end
            fcntl.flock(f, fcntl.LOCK_UN)

        print thiscookie
        print "Content-type: text/html\n\n"
        print "<h2>Welcome to the Staff Development Day!</h2>"
        print "<h3>You are the player number:",total_number,"</h3>"
        print "<h3>Your user name is:",thiscookie['name'].value,"</h3>"
        print "<h3><a href=\'../controller.html'>Go to the Controller!</a></h3>"
        print "And yes, we are watching you :<br>",user_agent,' - ',user_ip
else:
        print "Content-type: text/html\n\n"
        print "<h2>Welcome to the Staff Development Day!</h2>"
        print "<h3>You must insert a user name.</h3>"
        print "<h3><a href=\'../index.html'>Go back to register</a></h3>"        
    