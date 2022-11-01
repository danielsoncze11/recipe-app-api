"""
django command to wait for database to be available
"""
import time

from psycopg2 import OperationalError as Psycopg2OpError
from django.db.utils import OperationalError

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to wait for DB"""

    def handle(self, *args, **options):
        """Entrypoint for command"""
        # show in the console the message
        self.stdout.write('Waiting for DB...')
        db_up = False
        while db_up is False:
            try:
                # prikaz .check je z BaseCommand
                # kontroluje zda DB jede
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2OpError, OperationalError):
                self.stdout.write('Database unavailable, waiting 1 second')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('DB available!'))
