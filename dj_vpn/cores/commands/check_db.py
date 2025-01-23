import time

from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError


class Command(BaseCommand):
    help = "check database"

    def handle(self, *args, **options):
        postdb_conn = None
        print("start checking database")
        while not postdb_conn:
            try:
                postdb_conn = connections.databases['default']
            except OperationalError:
                print("database not found, waiting 1 seconds")
                time.sleep(1)
        print("database found", postdb_conn)
