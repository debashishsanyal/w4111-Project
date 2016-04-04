#!/usr/bin/env python2.7

"""
Reference: Columbia W4111 Intro to databases project
Authors: Debashish Hemant Sanyal (dhs2143)
         Apoorv Patwardhan (ap3341)

Dated: March 2016

To run locally

python server.py

Go to http://localhost:8111 in your browser



A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""

import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


#
# The following uses the sqlite3 database test.db -- you can use this for debugging purposes
# However for the project you will need to connect to your Part 2 database in order to use the
# data
#
# XXX: The URI should be in the format of:
#
#     postgresql://USER:PASSWORD@w4111db.eastus.cloudapp.azure.com/username
#
# For example, if you had username ewu2493, password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://ewu2493:foobar@w4111db.eastus.cloudapp.azure.com/ewu2493"
#
DATABASEURI = "postgresql://dhs2143:TZPGFH@w4111db.eastus.cloudapp.azure.com/dhs2143"
#DATABASEURI = "sqlite:///test.db"


#
# This line creates a database engine that knows how to connect to the URI above
#
engine = create_engine(DATABASEURI)

#
# START SQLITE SETUP CODE
#
# after these statements run, you should see a file test.db in your webserver/ directory
# this is a sqlite database that you can query like psql typing in the shell command line:
#
#     sqlite3 test.db
#
# The following sqlite3 commands may be useful:
#
#     .tables               -- will list the tables in the database
#     .schema <tablename>   -- print CREATE TABLE statement for table
#
# The setup code should be deleted once you switch to using the Part 2 postgresql database
#
#engine.execute("""DROP TABLE IF EXISTS test;""")
#engine.execute("""CREATE TABLE IF NOT EXISTS test (
#  id serial,
#  name text
#);""")
#engine.execute("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');""")
#
# END SQLITE SETUP CODE
#



@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request

  The variable g is globally accessible
  """
  try:
    g.conn = engine.connect()
  except:
    print "uh oh, problem connecting to database"
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to e.g., localhost:8111/foobar/ with POST or GET then you could use
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
#
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/')
def index():
  """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
  """

  # DEBUG: this is debugging code to see what request looks like
  print request.args


  #
  # example of a database query
  #
  cursor = g.conn.execute("SELECT name FROM users")
  names = []
  for result in cursor:
    names.append(result['name'])  # can also be accessed using result[0]
  cursor.close()
  #context = dict(data = names)
  #return render_template("index.html", **context)
  #
  # Flask uses Jinja templates, which is an extension to HTML where you can
  # pass data to a template and dynamically generate HTML based on the data
  # (you can think of it as simple PHP)
  # documentation: https://realpython.com/blog/python/primer-on-jinja-templating/
  #
  # You can see an example template in templates/index.html
  #
  # context are the variables that are passed to the template.
  # for example, "data" key in the context variable defined below will be
  # accessible as a variable in index.html:
  #
  #     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
  #     <div>{{data}}</div>
  #
  #     # creates a <div> tag for each element in data
  #     # will print:
  #     #
  #     #   <div>grace hopper</div>
  #     #   <div>alan turing</div>
  #     #   <div>ada lovelace</div>
  #     #
  #     {% for n in data %}
  #     <div>{{n}}</div>
  #     {% endfor %}
  #
  context = dict(data = names)


  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
  #context = dict(data = names)
  return render_template("index.html", **context)

#
# This is an example of a different path.  You can see it at
#
#     localhost:8111/another
#
# notice that the functio name is another() rather than index()
# the functions for each app.route needs to have different names
#
@app.route('/another')
def another():
  return render_template("anotherfile.html")


# Example of adding new data to the database
@app.route('/add', methods=['POST'])
def add():
  name = request.form['name']
  g.conn.execute('INSERT INTO test VALUES (NULL, ?)', name)
  return redirect('/')

########################################################################
########################################################################
########################################################################
########################################################################
######MAIN CODE STARTS##################################################
######MAIN CODE STARTS##################################################
########################################################################
########################################################################
########################################################################
########################################################################

@app.route('/goback')
def goback():
  return redirect('/')

############################ USERS part
############################ USERS part
############################ USERS part
############################ USERS part

#
@app.route('/user_search')
def user_search():
    """
    Goes to the html page where user search is done
    """

  uid = int(request.args.get('id', ''))
  name = str(request.args.get('name', ''))

  user_name = "%%"
  organization_name = "%%"
  r_interests = "%%"
  titles = "%%"

  #Find user(s) with the given search attributes
  cursor = g.conn.execute("SELECT * FROM users u WHERE u.name like %s and u.organization like %s and u.title like %s and u.r_interests like %s", user_name,organization_name,titles,r_interests)

  names = []
  for result in cursor:
    names.append(result)

  #only show results if there is at least one user in the database.
  headname = "No users in the database :-("
  colnames = []

  #only show results if there is at least one user in the database.
  if len(names) > 0:
      headname = "Users in the database:"
      colnames = [(u"Name",u"Research Interests",u"Organization",u"Title")]

  cursor.close()

  #log the details
  print names
  print colnames

  #Send data to html file
  context = dict(uid = uid,name = name,data = names,headname = headname,colnames = colnames)

  return render_template("user_search.html", **context)



@app.route('/find_user', methods=['POST'])
def find_user():
  """
  Finds user given the details
  """

  uid = int(request.form['uid'])
  name = str(request.form['namez'])

  #Get the details from the search input
  user_name = "%" + request.form['name'] + "%"
  organization_name = "%" + request.form['organization'] + "%"
  r_interests = "%" + request.form['r_interests'] + "%"
  titles = "%" + request.form['the_title'] + "%"

  #Find user(s) with the given search attributes
  cursor = g.conn.execute("SELECT * FROM users u WHERE u.name like %s and u.organization like %s and u.title like %s and u.r_interests like %s", user_name,organization_name,titles,r_interests)

  names = []
  for result in cursor:
    names.append(result)

  #only show results if there is at least one matching user.
  headname = "No users with the given attributes :("
  colnames = []

  #only show results if there is at least one matching user.
  if len(names) > 0:
      headname = "Matching user(s) are:"
      colnames = [(u"Name",u"Research Interests",u"Organization",u"Title")]

  cursor.close()

  #log the details
  print names
  print colnames

  #Send data to html file
  context = dict(uid = uid,name = name,data = names,headname = headname,colnames = colnames)
  return render_template("user_search.html", **context)


#Goes to the html file where user details are printed
@app.route('/user_details')
def user_details():

  ###TO RETURN TO USER HOMEPAGE
  uid = int(request.args.get('uid', ''))
  name = str(request.args.get('name', ''))

  #get the uid of the user whose details are to be printed
  uid1 = int(request.args.get('id', ''))

  print uid #logging in case debugging is required

  #cursor 2 gets details of the user. cursor 3 gets details of all users who cite THIS user.
  cursor1 = g.conn.execute("SELECT * FROM users u WHERE u.uid = %s", uid1) #My details
  cursor2 = g.conn.execute("SELECT u2.uid,u2.name,u2.r_interests,u2.organization,u2.title FROM User_cites us,users u2 WHERE us.uid2 = %s and us.uid1 = u2.uid", uid1) #who cited me
  cursor3 = g.conn.execute("SELECT u2.uid,u2.name,u2.r_interests,u2.organization,u2.title FROM User_cites us,users u2 WHERE us.uid1 = %s and us.uid2 = u2.uid", uid1) #I cited these people

  datas=[] #to store details of the main user
  citers = [] # to store details of the citer
  i_cited = []

  #getting details of the main user
  for result in cursor1:
    datas.append(result)

  #Getting details of the citers
  for result in cursor2:
    citers.append(result)
  total_citers = len(citers)

  #Getting details of the folks I (this user) cited.
  for result in cursor3:
    i_cited.append(result)
  total_cited = len(i_cited)

  #This is used for the table
  colnames_citers = []
  citers_head = ""
  colnames_cited = []
  cited_head = ""


  #Only print table if there indeed are people who have cited this user.
  if total_citers > 0:
      colnames_citers = [(u"Name",u"Research Interests",u"Organization",u"Title")]
      citers_head =  "The user has been cited by: "

  if total_cited > 0:
      colnames_cited = [(u"Name",u"Research Interests",u"Organization",u"Title")]
      cited_head =  "The user cited: "


  context = dict(name = name,uid = uid,data = datas,citers = citers,i_cited = i_cited,total_citers = total_citers,total_cited = total_cited,colnames_citers = colnames_citers,colnames_cited = colnames_cited,citers_head = citers_head,cited_head = cited_head)
  return render_template("user_details.html", **context)


############################ PUBLICATIONS part
############################ PUBLICATIONS part
############################ PUBLICATIONS part
############################ PUBLICATIONS part

#Goes to the html file where publication search is done
@app.route('/publication_search')
def publication_search():

   uid = int(request.args.get('id', ''))
   name = str(request.args.get('name', ''))

   #Find all publication(s)
   cursor = g.conn.execute("SELECT * FROM Publications");
   names = []
   for result in cursor:
     names.append(result)

   #only show results if there is at least one publication in the database.
   headname = "No publications in the database :-("
   colnames = []

   #only show results if there is at least one publicaiton in the database..
   if len(names) > 0:
     headname = "Publication(s) in the database are:"
     colnames = [(u"Title",u"DOI",u"Type")]

   cursor.close()

   #log the details
   print names
   print colnames

   #Send data to html file
   context = dict(uid = uid,name = name,data = names,headname = headname,colnames = colnames)
   return render_template("publication_search.html", **context)


# n
@app.route('/find_publication', methods=['POST'])
def find_publication():
  """
  Logic for finding the publication, given the search attributes.
  """
  #FOR GOING BACK TO USER HOME PAGE
  uid = int(request.form['uid'])
  name = str(request.form['namez'])

  #Get the details of all publications
  pub_title = "%" + request.form['title'] + "%"
  pub_doi = "%" + request.form['doi'] + "%"
  pub_type = "%" + request.form['type'] + "%"

  print pub_title
  print pub_doi
  print pub_type

  #Find publication(s) with the given search attributes
  cursor = g.conn.execute("SELECT * FROM Publications P WHERE P.title like %s and P.doi like %s and P.type like %s", pub_title,pub_doi,pub_type)

  names = []
  for result in cursor:
    names.append(result)

  #only show results if there is at least one matching publication.
  headname = "No publications with the given attributes ... try again"
  colnames = []

  #only show results if there is at least one matching publication.
  if len(names) > 0:
    headname = "Matching publication(s) are:"
    colnames = [(u"Title",u"DOI",u"Type")]

  cursor.close()

  #log the details
  print names
  print colnames

  #Send data to html file
  context = dict(uid = uid,name = name,data = names,headname = headname,colnames = colnames)
  return render_template("publication_search.html", **context)

@app.route('/publication_details')
def publication_details():
  """
  Goes to the page where publication details are printed.
  """
  ###TO RETURN TO USER HOMEPAGE
  uid = int(request.args.get('uid', ''))
  name = str(request.args.get('name', ''))

  #get the pid of the publication whose details are to be printed
  pid = int(request.args.get('id', ''))
  print pid #logging in case debugging is required

  #cursor1 gets details of the publication. cursor2 gets details of all publications who cite THIS publication.
  cursor1 = g.conn.execute("SELECT * FROM Publications P WHERE P.pid = %s", pid)
  cursor2 = g.conn.execute("SELECT u2.title,u2.citations,u2.field,u2.doi,u2.type, u2.pid FROM Publication_cites us,Publications u2 WHERE us.pid2 = %s and us.pid1 = u2.pid", pid) #who cited me
  # Get details of all publications which this publications cites
  cursor3 = g.conn.execute("Select * from (Select pid2 from Publication_cites where pid1=%s) AS D INNER JOIN Publications P ON (D.pid2=P.pid)", pid)
  # Get the venue at which the publication is published
  cursor4 = g.conn.execute("Select * from (Select vid from Published_or_Presented_at where pid = %s) AS D INNER JOIN Venues V ON (V.vid=D.vid)",pid)
  # Get the authors
  cursor5 = g.conn.execute("Select * from (Select uid from Published where pid = %s) AS D INNER JOIN Users U ON (U.uid=D.uid)",pid)
  datas=[] #to store details of the main user
  citers = [] # to store details of the citer
  thispub_cited = []
  venue_info=[] # to store venue
  author_info=[] # to store authors

  #getting details of the main user
  for result in cursor1:
    datas.append(result)

  #Getting details of the citers
  for result in cursor2:
    citers.append(result)
  total_citers = len(citers)

  for result in cursor3:
    thispub_cited.append(result)
  total_cited = len(thispub_cited)

  for result in cursor4:
    venue_info.append(result)
  for result in cursor5:
    author_info.append(result)


  #This is used for the table
  colnames_citers = []
  citers_head = ""
  colnames_cited = []
  cited_head = ""
  colnames_venueinfo = [(u"Journal Title", u"Conference Title", u"Location", u"Sponsor")]
  #Only print table if there indeed are publications who have cited this publication.
  if total_citers > 0:
      colnames_citers = [(u"Title",u"DOI",u"Type")]
      citers_head =  "This publication has been cited by: "

  if total_cited>0:
    colnames_cited = [(u"Title",u"DOI",u"Type")]
    cited_head = "This publication cites the following publications:"

  context = dict(name = name,uid = uid,data = datas,citers = citers,total_citers = total_citers,colnames_citers = colnames_citers,citers_head = citers_head, colnames_cited = colnames_cited, total_cited=total_cited,cited_head=cited_head, thispub_cited=thispub_cited, venue_info = venue_info, colnames_venueinfo = colnames_venueinfo, author_info=author_info)
  print thispub_cited
  return render_template("publication_details.html", **context)


############################ Venue part
############################ Venue part
############################ Venue part
############################ Venue part



@app.route('/venue_search')
def venue_search():
  """
  #Goes to the html file where venue search is done
  """
  uid = int(request.args.get('id', ''))
  name = str(request.args.get('name', ''))

  #Find all venue(s)
  cursor = g.conn.execute("SELECT * FROM Venues V")
  names = []
  for result in cursor:
    names.append(result)

  #only show results if there is at least Venue in the database.
  headname = "No venues in the database :("
  colnames = []

  #only show results if there is at least Venue in the database.
  if len(names) > 0:
      headname = "Venue(s) in the database are:"
      colnames = [(u"Journal Title",u"Conference Title",u"Location",u"Type",u"Sponsor")]

  cursor.close()

  #log the details
  print names
  print colnames

  #Send data to html file
  context = dict(uid = uid,name = name,data = names,headname = headname,colnames = colnames)

  return render_template("venue_search.html", **context)

@app.route('/find_venue', methods=['POST'])
def find_venue():
  """
  Finds the venue, given the search attributes.
  """

  uid = int(request.form['uid'])
  name = str(request.form['namez'])

  #Get the details from the search input
  venue_journaltitle = "%" + request.form['journal_title'] + "%"
  venue_conftitle = "%" + request.form['conference_title'] + "%"
  venue_location = "%" + request.form['location'] + "%"
  venue_type = "%" + request.form['type'] + "%"
  venue_sponsor = "%" + request.form['sponsor'] + "%"

  print venue_journaltitle
  print venue_conftitle
  print venue_location
  print venue_type
  print venue_sponsor

  #Find venue(s) with the given search attributes
  cursor = g.conn.execute("SELECT * FROM Venues V WHERE V.journal_title like %s and V.conference_title like %s and V.location like %s and V.type like %s and V.sponsor like %s", venue_journaltitle,venue_conftitle,venue_location,venue_type,venue_sponsor)
  #cursor = g.conn.execute("SELECT * FROM Venues V")
  names = []
  for result in cursor:
    names.append(result)

  #only show results if there is at least one matching Venue.
  headname = "No venues with the given attributes :("
  colnames = []

  #only show results if there is at least one matching Venue.
  if len(names) > 0:
      headname = "Matching venue(s) are:"
      colnames = [(u"Journal Title",u"Conference Title",u"Location",u"Type",u"Sponsor")]

  cursor.close()

  #log the details
  print names
  print colnames

  #Send data to html file
  context = dict(uid = uid,name = name,data = names,headname = headname,colnames = colnames)

  return render_template("venue_search.html", **context)

#Goes to the html file where Venue details are printed
@app.route('/venue_details')
def venue_details():
  """
  Prints the details of the given Venue
  """
  ###ADD THESE 2 LINES, AND THE RELEVANT CONTEXT, TO ALL YOUR SEARCH PAGES, TO RETURN TO USER HOMEPAGE
  uid = int(request.args.get('uid', ''))
  name = str(request.args.get('name', ''))

  #get the vid of the venue whose details are to be printed
  vid = int(request.args.get('id', ''))
  print vid #logging in case debugging is required

  #cursor 1 gets details of the venue. cursor 2 gets details of all users who cite THIS user.
  cursor1 = g.conn.execute("SELECT * FROM Venues V WHERE V.vid = %s", vid)
  # Get the names of all users who attended the conference
  cursor2 = g.conn.execute("Select * from (Select A.uid from Attended_by A Where A.vid=%s) AS D INNER JOIN Users U ON (U.uid=D.uid)", vid) #who cited me
  # Get the names of all people who published in journals
  cursor3 = g.conn.execute("Select * from (Select K.uid from Known_contributors K Where K.vid=%s) AS D INNER JOIN Users U ON (U.uid=D.uid)", vid) #I cited these people
  # Get the type of venue
  cursor4 = g.conn.execute("Select type from Venues where vid= %s ", vid)
  # Get the details of the publications which got published in venue
  cursor5 = g.conn.execute("Select * from (Select pid from Published_or_Presented_at where vid= %s) AS D INNER JOIN Publications P ON (D.pid=P.pid)",vid)


  datas=[] #to store details of the main user
  visitors = [] # to store details of the citer
  venuetype = []
  publications = [] # store the published articles

  #getting details of the main user
  for result in cursor1:
    datas.append(result)

  # getting visitor details
  for result in cursor2:
    visitors.append(result)
  for result in cursor3:
    visitors.append(result)
  total_visitors = len(visitors)

  for result in cursor4:
    venuetype.append(result)

  for result in cursor5:
    publications.append(result)
  total_articles = len(publications)

  colnames_visitors=[]
  if total_visitors>0:
    colnames_visitors=[(u"Name",u"Title",u"Organization")]
  colnames_publications=[]
  if total_articles>0:
    colnames_publications=[(u"Title",u"DOI",u"Field")]

  context = dict(name = name,uid = uid,data = datas, visitors=visitors, total_visitors = total_visitors, colnames_visitors = colnames_visitors, venuetype=venuetype, publications=publications,colnames_publications=colnames_publications, total_articles = total_articles)
  #context = dict(data=datas)
  #print this
  return render_template("venue_details.html", **context)



############################ ADDING A NEW USER
############################ ADDING A NEW USER
############################ ADDING A NEW USER
############################ ADDING A NEW USER
############################ ADDING A NEW USER
############################ ADDING A NEW USER
############################ ADDING A NEW USER

@app.route('/user_add')
def user_add():
  return render_template("user_add.html")


@app.route('/add_user', methods=['POST'])
def add_user():
    """
    Gets details of user to be added from the form and inserts details into database
    """
    user_name = request.form['name']
    organization_name = request.form['organization']
    r_interests = request.form['r_interests']
    titles = request.form['the_title']
    assoc = request.form['associations']
    desc = request.form['description']
    types = request.form['type']
    uname = request.form['username']
    pwd = request.form['password']

    #user_name = "SNOOP DOG"
    #organization_name = "RAPPERS"
    #r_interests = "RAPPING"
    #titles = "King"
    #assoc = "Them rappers"
    #desc = "I rap real good"
    #types = "Academician"


    uname = request.form['username']
    pwd = request.form['password']

    #Check if the username is already in the table
    cursor = g.conn.execute("SELECT uid,name FROM users where username = %s",uname)

    to_check = []
    for result in cursor:
      uid = result[0]
      name = result[1]
      to_check.append(result)

    cursor.close()

    #we want len to be 0, because that means that there isnt a duplicate username. Awesome.
    if len(to_check) == 0:
        #GET MAX UID
        cursor1 = g.conn.execute("SELECT max(uid) from users")
        for stuff in cursor1:
            uid = stuff[0] + 1
        #Add user to the database
        engine.execute("INSERT into users values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",uid,types,r_interests,desc,user_name,assoc,titles,organization_name,uname,pwd)
        added_message = "User added!"
        cursor1.close()
        context = dict(added_message = added_message)
        return render_template("user_add.html", **context)
    else:
        headname1 = "username already exists! Please type in a different username."
        context = dict(headname1 = headname1)
        return render_template("user_add.html", **context)




############################ LOGIN, AND STUFF A USER CAN DO AFTER LOGGING IN
############################ LOGIN, AND STUFF A USER CAN DO AFTER LOGGING IN
############################ LOGIN, AND STUFF A USER CAN DO AFTER LOGGING IN
############################ LOGIN, AND STUFF A USER CAN DO AFTER LOGGING IN
############################ LOGIN, AND STUFF A USER CAN DO AFTER LOGGING IN
############################ LOGIN, AND STUFF A USER CAN DO AFTER LOGGING IN
############################ LOGIN, AND STUFF A USER CAN DO AFTER LOGGING IN
############################ LOGIN, AND STUFF A USER CAN DO AFTER LOGGING IN
############################ LOGIN, AND STUFF A USER CAN DO AFTER LOGGING IN
############################ LOGIN, AND STUFF A USER CAN DO AFTER LOGGING IN
############################ LOGIN, AND STUFF A USER CAN DO AFTER LOGGING IN
############################ LOGIN, AND STUFF A USER CAN DO AFTER LOGGING IN

#Goes to the html file where user is added



@app.route('/login')
def login():
    """
    #OPENS THE LOGIN PAGE
    """
    cursor = g.conn.execute("SELECT name FROM users")
    names = []
    for result in cursor:
      names.append(result['name'])  # can also be accessed using result[0]
    cursor.close()
    context = dict(data = names)
    return render_template("login.html", **context)


@app.route('/return_logged_in')
def return_logged_in():
    """
    #ALLOWS USER TO RETURN TO HIS OR HER HOMEPAGE
    """
    uid = int(request.args.get('uid', ''))
    namez = str(request.args.get('name', ''))
    message = ""
    context = dict(name = namez,uid = uid,message = message)
    return render_template("logged_in.html", **context)

@app.route('/check_login', methods=['POST'])
def check_login():
    """
    #CHECKS IF LOGIN CREDENTIALS ARE CORRECT
    """
    uname = request.form['username']
    pwd = request.form['password']
    cursor = g.conn.execute("SELECT uid,name FROM users where username = %s and password = %s",uname, pwd)
    print "here"
    to_check = []
    for result in cursor:
      uid = result[0]
      name = result[1]
      to_check.append(result)
    print "here22"
    if len(to_check) == 0:
        print "here444"
        message = "Incorrect credentials, please try again."
        context = dict(message = message)
        return render_template("login.html", **context)
    else:
        print uid
        print name
        message = ""
        context = dict(name = name,uid = uid,message = message)
        return render_template("logged_in.html", **context)


@app.route('/user_change_details')
def user_change_details():
  """
  #ALLOWS USER TO CHANGE HIS DETAILS/ATTRIBUTES, DIRECTS HIM TO THE PAGE WHERE HE CAN DO THIS
  """
  uid = int(request.args.get('id', ''))
  namez = str(request.args.get('name', ''))

  datas = []
  cursor1 = g.conn.execute("SELECT * FROM users u WHERE u.uid = %s", uid)
  for result in cursor1:
    datas.append(result)

  context = dict(data = datas,uid = uid,name = namez)
  return render_template("user_change_details.html", **context)


@app.route('/user_make_changes',methods=['POST'])
def user_make_changes():
  """
  # IMPLEMENTS THE CHANGES ENTERED BY THE USER AND RETURNS TO USERS HOME PAGE
  """
  user_name = request.form['name']
  organization_name = request.form['organization']
  r_interests = request.form['r_interests']
  titles = request.form['the_title']
  assoc = request.form['associations']
  desc = request.form['description']
  uname = request.form['username']
  pwd = request.form['password']

  uid = int(request.form['uid'])
  namez = request.form['original_name']


  if len(user_name) > 0:
      engine.execute("UPDATE users set name = %s where uid = %s",user_name,uid)
      namez = user_name

  if len(organization_name) > 0:
      engine.execute("UPDATE users set organization = %s where uid = %s",organization_name,uid)

  if len(r_interests) > 0:
      engine.execute("UPDATE users set r_interests = %s where uid = %s",r_interests,uid)

  if len(titles) > 0:
      engine.execute("UPDATE users set title = %s where uid = %s",titles,uid)

  if len(assoc) > 0:
      engine.execute("UPDATE users set assoc = %s where uid = %s",assoc,uid)

  if len(desc) > 0:
      engine.execute("UPDATE users set description = %s where uid = %s",desc,uid)

  if len(uname) > 0:
      engine.execute("UPDATE users set username = %s where uid = %s",uname,uid)

  if len(pwd) > 0:
      engine.execute("UPDATE users set password = %s where uid = %s",pwd,uid)



  message = "User details updated."
  context = dict(name = namez,uid = uid,message = message)
  return render_template("logged_in.html", **context)



#WE DONT BE USING THE NEXT 3 FUNCTIONS, KEPT THEM JUST IN CASE
#WE DONT BE USING THE NEXT 3 FUNCTIONS, KEPT THEM JUST IN CASE
#WE DONT BE USING THE NEXT 3 FUNCTIONS, KEPT THEM JUST IN CASE
#WE DONT BE USING THE NEXT 3 FUNCTIONS, KEPT THEM JUST IN CASE


#WE DONT BE USING THIS FUNCTION
#Goes to the html file where one can search for a user to be deleted
@app.route('/user_remove')
def user_remove():
  return render_template("user_remove.html")

#WE WONT BE USING THIS FUNCTION
# Finds the user to delete
@app.route('/find_remove_user', methods=['POST'])
def find_remove_user():
    #Send data to html file
    #Get the details from the search input
    user_name = "%" + request.form['name'] + "%"
    organization_name = "%" + request.form['organization'] + "%"
    r_interests = "%" + request.form['r_interests'] + "%"
    titles = "%" + request.form['the_title'] + "%"

    #Find user(s) with the given search attributes
    cursor = g.conn.execute("SELECT * FROM users u WHERE u.name like %s and u.organization like %s and u.title like %s and u.r_interests like %s", user_name,organization_name,titles,r_interests)

    names = []
    for result in cursor:
      names.append(result)

    #only show results if there is at least one matching user.
    headname = "No users with the given attributes :("
    colnames = []

    #only show results if there is at least one matching user.
    if len(names) > 0:
        headname = "Click on the user you want to remove:"
        colnames = [(u"Name",u"Research Interests",u"Organization",u"Title")]

    cursor.close()

    #log the details
    print names
    print colnames

    #Send data to html file
    context = dict(data = names,headname = headname,colnames = colnames)
    return render_template("user_remove.html", **context)

#WE WONT BE USING THE FUNCTION
#Deletes the selected user
@app.route('/remove_user')
def remove_user():

  #get the uid of the user whose details are to be printed
  uid = int(request.args.get('id', ''))
  namez = str(request.args.get('name', ''))

  print uid #logging in case debugging is required
  g.conn.execute("DELETE from users where uid = %s",uid)

  #these messages will be printed only after deletion
  headname = "User (" + namez + ") deleted."
  colnames = []
  names = []
  context = dict(data = names,headname = headname,colnames = colnames)
  return render_template("user_remove.html", **context)

#FOLLOWING FUNCTIONS, WE WILL BE USING.
#FOLLOWING FUNCTIONS, WE WILL BE USING.
#FOLLOWING FUNCTIONS, WE WILL BE USING.
#FOLLOWING FUNCTIONS, WE WILL BE USING.



@app.route('/remove_user2')
def remove_user2():
  """
  #Deletes the user who is logged in (ONLY A LOGGED IN USER MAY DELETE HIMSELF OR HERSELF, SO WE WILL BE USING THIS)
  """
  uid = int(request.args.get('id', ''))
  namez = str(request.args.get('name', ''))

  print uid
  g.conn.execute("DELETE from users where uid = %s",uid)

  #these messages will be printed only after deletion
  headname = "User (" + namez + ") deleted."
  print "Hereee"
  context = dict(headname = headname)
  return render_template("index.html", **context)



@app.route('/publication_remove')
def publication_remove():
    """
    LISTS DOWN THE USERS PUBLICATIONS AND renders it, so that the user may choose one and delete
    """
    uid = int(request.args.get('id', ''))
    namez = str(request.args.get('name', ''))

    #Find pyblications(s) of this user
    cursor = g.conn.execute("SELECT p.doi,p.title,p.pid from users u,publications p,published pb where u.uid = pb.uid and pb.pid = p.pid and u.uid = %s",uid);

    names = []
    for result in cursor:
      names.append(result)

    #only show results if there is at least one matching publication.
    headname1 = "You have no publications to delete :("
    colnames = []

    #only show results if there is at least one matching publication.
    if len(names) > 0:
        headname1 = "Click on the publication you want to remove:"
        colnames = [(u"doi",u"Title")]

    cursor.close()

    #log the details
    print names
    print colnames

    #Send data to html file
    context = dict(data = names,headname1 = headname1,colnames = colnames,uid = uid,name = namez)
    return render_template("publication_remove.html", **context)



@app.route('/remove_publication')
def remove_publication():
  """
  #DELETES THE PUBLICATION SELECTED BY THE USER
  """

  print "here0"
  uid = int(request.args.get('uid', ''))
  print "here1"
  pid = int(request.args.get('pid', ''))
  print "here2"
  namez = str(request.args.get('name', ''))
  print "here3"
  title = str(request.args.get('title', ''))
  print "here4"
  print uid #logging in case debugging is required
  print "here5"
  g.conn.execute("DELETE from publications where pid = %s",pid)
  print "here6"

  message = "Publication (" + title + ") deleted!"
  context = dict(name = namez,uid = uid,message = message)
  return render_template("logged_in.html", **context)


@app.route('/publication_add')
def publication_add():
  """
  #DIRECTS USER TO THE PAGE WHERE THE USER CAN ADD A NEW PUBLICATION
  """
  uid = int(request.args.get('id', ''))
  namez = str(request.args.get('name', ''))

  context = dict(name = namez,uid = uid)
  return render_template("publication_add.html", **context)


@app.route('/add_publication', methods=['POST'])
def add_publication():
    """
    #ADDS THE PUBLICATION BY USING THE DETAILS ENTERED BY THE USER
    """
    uid = int(request.form['uid'])
    name = request.form['name']

    title = request.form['title']
    citations = int(request.form['citations'])
    field = request.form['field']
    doi = request.form['doi']
    types = request.form['type']
    advisor = request.form['advisor']
    patent_office = request.form['patent_office']
    patent_no = request.form['patent_no']

    #GET MAX PID
    cursor1 = g.conn.execute("SELECT max(pid) from publications")
    for stuff in cursor1:
        pid = stuff[0] + 1


    print "here before insert"
    engine.execute("INSERT into publications values (%s,%s,%s,%s,%s,%s,%s,%s,%s)",title,citations,pid,field,doi,types,advisor,patent_office,patent_no)
    print "here after insert1"
    engine.execute("INSERT into Published values (%s,%s,%s)",uid,pid,types);
    print "here after insert2"

    message = "Publication (" + title + ") added!"
    context = dict(name = name,uid = uid,message = message)
    return render_template("logged_in.html", **context)




if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default= 8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using

        python server.py

    Show the help text using

        python server.py --help

    """

    HOST, PORT = host, port
    print "running on %s:%d" % (HOST, PORT)
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()
