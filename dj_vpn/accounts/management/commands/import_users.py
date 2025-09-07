import csv
from dj_vpn.accounts.models import User
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Import users from a CSV file"

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str, help="path to the CSV file")

    def handle(self, *args, **options):
        try:
            csv_file = options["csv_file"]
            users = []
            with open(csv_file) as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    users.append(
                        User(
                            mobile_phone=row["mobile_phone"],
                            birth_date=row['birth_date'],
                            account_type=row["account_type"],
                            accounts_status=row["accounts_status"],
                            volume_choice=row["volume_choice"],
                            volume=row["volume"],
                            volume_usage=row["volume_usage"],
                            is_inf_volume=row['is_inf_volume'],
                            all_volume_usage=row['all_volume_usage'],
                            start_premium=row['start_premium'],
                            number_of_days=row['number_of_days'],
                            number_of_login=row['number_of_login'],
                            number_of_max_device=row['number_of_max_device'],
                            fcm_token=row['fcm_token'],
                            is_connected_user=row['is_connected_user'],
                            password=row['password'],
                            user_type=row['user_type'],
                            created_by_id=row['created_by_id'],
                        )
                    )
            if users:
                User.objects.bulk_create(users)
                self.stdout.write("successfully imported {} users".format(len(users)))
        except Exception as e:
            raise CommandError(e)
