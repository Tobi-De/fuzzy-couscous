Database Tips
=============

django-pgtriggers
-----------------

Database backup
---------------

Whenever possible, take advantage of a fully managed database solution, they usually offer automatic backup of your databases.
In my opinion, this is the best option if you don’t want to deal with the hassle of managing your own database.

-  `Amazon RDS <https://aws.amazon.com/rds/>`__
-  `Linode Managed Databases <https://www.linode.com/products/databases/>`__
-  `DigitalOcean Managed Databases <https://www.digitalocean.com/products/managed-databases>`__
-  `Heroku postgres <https://www.heroku.com/postgres>`__

For specific postgresql options, see their `hosting support page <https://www.postgresql.org/support/professional_hosting/>`__.

However, if for some reason you want / need to manage your database yourself and just want an automatic backup solution
then `django-dbbackup <https://github.com/jazzband/django-dbbackup>`__ is what you need. You can use one of the scheduling
packages discussed above to periodically run the backup command.

Scaling strategies
------------------

This is mosty a buzz work, people use that term to represent app that can handle thousands millions of requests per second.
Scalability is a problem you want to have (that's mean you've make it), but people are out there solving scalability issues for 
app that has not even being ship, class chicken and egg problem.
I don't have enough personal experiences here to give good advices but I'll try to give some pointers based on what I've read and
the little experience I have (app I've seen even if not worked on).
I put this section here (in the databases guide) because it seems that more often than not, the database is the bottleneck, or at least
before django or python become a bottleneck to you, your database will be the first to be a bottleneck. Maybe not the database itself at
first, how you access it and how your queries are writter, for that checkout the `database optimization section </guides/optimizing_database_access.html>`__.
Both of these section are complemantary.

For most of these stratgies I'll assume you are using postgresql, because that's what I know best, but most of these strategies can be applied to other databases.


Offload work from the database
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Table partitionning
^^^^^^^^^^^^^^^^^^^

Read replicas
^^^^^^^^^^^^^

Sharding
^^^^^^^^
