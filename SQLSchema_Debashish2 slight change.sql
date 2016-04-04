/*
W4111 002- Introduction to Databases, Columbia University
Project, Part 2
SQL Schema
Members: Apoorv Prakash Pathwardhan (UNI ap3341), Debashish Hemant Sanyal (UNI dhs2143)
*/

-- USERS

CREATE TABLE Users(
  uid int,
  type text NOT NULL,

  r_interests text NOT NULL,
  description text NOT NULL,
  name text NOT NULL,
  assoc text, -- Associations of the user (e.g. IEEE, etc)

  title text, -- Company position, professor, etc
  organization text, -- company name, university name

  CHECK( ((type = 'Academician' OR type = 'Company_RS') AND title IS NOT NULL AND
            organization IS NOT NULL
         )
          OR
           type = 'Independent_RS'
       ),
  PRIMARY KEY (uid)
);


--########################################################################
--########################################################################
--########################################################################

-- PUBLICATIONS

CREATE TABLE Publications(
  title text NOT NULL,
  citations int,
  pid int,
  field text NOT NULL,
  doi text NOT NULL,

  type text,

  --Thesis
  advisor text,

  -- Research_Articles

  --Patents
  patent_office text,
  patent_no text,

  CHECK((type = 'Thesis' AND advisor IS NOT NULL) OR (type = 'Research article' AND
  patent_office IS NULL AND patent_no IS NULL) OR (type = 'Patent' AND
  patent_office IS NOT NULL AND patent_no IS NOT NULL)),

  PRIMARY KEY (pid,type), --type is later used to distinguish type when referenced by 'presented_at'
  UNIQUE (pid)
);


--########################################################################
--########################################################################
--########################################################################

-- VENUES

CREATE TABLE Venues(
  vid int,
  fields text,
  impact numeric,
  type text,

  journal_title text,

  conference_title text,
  location text,
  sponsor text,


  CHECK(
          (type = 'Journal' AND journal_title IS NOT NULL AND conference_title IS NULL AND location IS NULL AND sponsor IS NULL)
          OR
          (type = 'Conference' AND conference_title IS NOT NULL AND location IS NOT NULL AND sponsor IS NOT NULL
            AND journal_title IS NULL
          )
       ),
  PRIMARY KEY (vid,type), -- to distinguish type when referenced by 'attended_by' and 'known_contributors'
  UNIQUE (vid)
);


--########################################################################
--########################################################################
--########################################################################

-- RELATIONS ("AT LEAST ONE" relation not expressed)

CREATE TABLE Published(
  uid int,
  pid int,
  ptype text,

  PRIMARY KEY (uid,pid,ptype), -- A user can have multiple publications, A publication may have multiple users
  FOREIGN KEY (uid) REFERENCES Users ON DELETE CASCADE,
  FOREIGN KEY (pid,ptype) REFERENCES Publications ON DELETE CASCADE
);


CREATE TABLE Published_or_Presented_at(
  vid int NOT NULL,
  vtype text,
  pid int,
  ptype text,

  CHECK(ptype = 'Research article'),
  PRIMARY KEY (pid), -- A venue may host multiple publications, a publication may be hosted at multiple venues
  FOREIGN KEY (vid,vtype) REFERENCES Venues ON DELETE CASCADE,
  FOREIGN KEY (pid,ptype) REFERENCES Publications ON DELETE CASCADE
);

CREATE TABLE Attended_by (
  vid int,
  vtype text,
  uid int,

  FOREIGN KEY (vid,vtype) REFERENCES Venues ON DELETE CASCADE,
  FOREIGN KEY (uid) REFERENCES Users ON DELETE CASCADE,
  CHECK (vtype = 'Conference'),
  PRIMARY KEY (vid,uid) -- A conference may be attended by may users, a user may attend many conferences

);

CREATE TABLE Known_contributors(
  vid int,
  vtype text,
  uid int,

  FOREIGN KEY (vid,vtype) REFERENCES Venues ON DELETE CASCADE,
  CHECK (vtype = 'Journal'),
  FOREIGN KEY (uid) REFERENCES Users ON DELETE CASCADE,
  PRIMARY KEY (vid,uid) -- A journal may have many users as contributers, a user may contribute to multiple journals

);

CREATE TABLE User_cites(
  uid1 int,
  uid2 int,

  FOREIGN KEY (uid1) REFERENCES Users ON DELETE CASCADE,
  FOREIGN KEY (uid2) REFERENCES Users ON DELETE CASCADE,
  PRIMARY KEY (uid1,uid2)
);

CREATE TABLE Publication_cites(
  pid1 int,
  pid2 int,

  PRIMARY KEY (pid1,pid2),
  FOREIGN KEY (pid1) REFERENCES Publications (pid) ON DELETE CASCADE,
  FOREIGN KEY (pid2) REFERENCES Publications (pid) ON DELETE CASCADE
);
