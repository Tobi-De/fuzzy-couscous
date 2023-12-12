## Intro


## django-pgtriggers


## Database backup

Whenever possible, take advantage of a fully managed database solution, they usually offer automatic backup of your databases.
In my opinion, this is the best option if you don't want to deal with the hassle of managing your own database.

- [Amazon RDS](https://aws.amazon.com/rds/)
- [Linode Managed Databases](https://www.linode.com/products/databases/)
- [DigitalOcean Managed Databases](https://www.digitalocean.com/products/managed-databases)
- [Heroku postgres](https://www.heroku.com/postgres)

For specific postgresql options, see their [hosting support page](https://www.postgresql.org/support/professional_hosting/).

However, if for some reason you want / need to manage your database yourself and just want an automatic backup solution
then [django-dbbackup](https://github.com/jazzband/django-dbbackup) is what you need. You can use one of the scheduling
packages discussed above to periodically run the backup command.


## Scaling strategies