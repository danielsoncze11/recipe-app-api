"""Test custom Django management commands."""

from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2Error

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


# mocking the command with the patch...for all tests within this class
# budeme pouzivat Command.check coz je metoda BaseCommand ktery byl pouzit
# v fce Command. Budeme mocking the check metod aby jsme simulovali
# tu check metod ktera bud return exception nebo value
@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test commands."""

    # protoze jsme dali patch k te hlavni class..tak to doda argument ke
    # kazde fci..patched_check (je to obj ktery nahrani check z base command)
    #  a muzeme customizovat jeho chovani
    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for DB if DB ready."""
        # kdyz ta methoda check je zavolana...tak jne vrati value True
        patched_check.return_value = True

        # timto udelame call command..to runnje kod v wait_for_db
        # to testuje jestli ten command je set up correctly a vubec
        # muze byt volan v Django app....a potom taky
        # jeho vysledek..jestli je db ready
        call_command('wait_for_db')

        # timto kontrolujeme jestli ten .patched_check metod byl vubec zavolan
        # to zajistuje ze ta methoda byla zavolana s parametry...database=..
        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for DB when getting operational error"""

        patched_check.side_effect = [Psycopg2Error] * 2 + \
                                    [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
