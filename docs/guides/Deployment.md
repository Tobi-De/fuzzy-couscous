This template was configured to simplify deployment on [caprover](https://caprover.com/), since that is what I use 99% of the time.

!!! Quote
    CapRover is an extremely easy to use app/database deployment & web server manager for your NodeJS, Python, PHP, ASP.NET, Ruby, MySQL, MongoDB, Postgres, WordPress (and etc...) applications!

    **Official site**

CapRover is a self-hosted [PaaS](https://en.wikipedia.org/wiki/Platform_as_a_service) solution, think [heroku](https://www.heroku.com/) but on your own servers.
Nowadays, I tend to prefer PaaS solutions over manual deployment and configuration, as they are easy to use with little configuration to deploy most apps.
Software is usually quite a pain to deploy and even though I've gotten better at it over time, I'll always choose a managed solution over manual deployment.
Some other options than **CapRover** are:

- [Dokku](https://dokku.com/) (self hosted)
- [Fly](https://fly.io/) (hosted)
- [Render](https://render.com/) (hosted)
- [Coolify](https://github.com/coollabsio/coolify) (self hosted)
- [DigitalOcean App Platform](https://www.digitalocean.com/products/app-platform) (hosted)
- [AWS Elastic Beanstalk](https://aws.amazon.com/elasticbeanstalk/) (hosted)
- [Btn](https://btn.dev/) (hosted and not ready yet)

!!! Info
    I recently discovered [django-simple-deploy](https://github.com/ehmatthes/django-simple-deploy) which can configure your django project for some of the alternatives to
    caprover I listed above.

I find that self-hosted solutions are generally cheaper than managed/hosted solutions, but I don't have much experience with managed solutions,
so I could be wrong, do your own research and if you can afford it, try them out to see what works best for you.

After installing CaProver with the [getting started guide](https://caprover.com/docs/get-started.html), there is not much left to do, create a new application and in the section `deployment`.
configure your application using the third method `Method 3: Deploy from Github/Bitbucket/Gitlab`.

!!! Info
    If you use github, instead of entering your password directly into the `password` field, you can use a [personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token),
    which is a more secure option.

!!! Tip
    Checkout [caprover automatic deploy](https://caprover.com/docs/deployment-methods.html#automatic-deploy-using-github-bitbucket-and-etc) to automate the deployment of your applications.
