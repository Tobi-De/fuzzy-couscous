from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = (
        "Clean up all installed application migrations, intended only for development."
    )

    def handle(self, *args, **options):
        if not settings.DEBUG:
            return self.stdout.write(
                self.style.WARNING("Nope, that won't happen here :)")
            )
        excludes = ["__init__.py"]
        apps = set()
        for folder in settings.APPS_DIR.iterdir():
            migration_dir = folder / "migrations"
            if not migration_dir.exists():
                continue
            for file in migration_dir.iterdir():
                if file.suffix == ".py" and file.name not in excludes:
                    file.unlink()
                    apps.add(str(folder))
                    self.stdout.write(self.style.NOTICE(f"{str(file)} deleted"))
        apps_ = ", ".join(apps)
        self.stdout.write(
            self.style.SUCCESS(f"\nRemoved migration files for apps: {apps_}")
        )
