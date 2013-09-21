# coding=utf-8

import os
import subprocess
from django.conf import settings

from django.core.management.base import BaseCommand

CURRDIR = os.path.dirname(__name__)

DATADIR = os.path.join(CURRDIR, 'data')

class Command(BaseCommand):

    def handle(self, *args, **options):

        subprocess.check_call(
            ['psql', '-f', 'zaj1.sql', settings.ZAJ1_DATABASE],
            cwd=DATADIR
        )
