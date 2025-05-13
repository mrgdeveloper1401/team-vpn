from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError
import psycopg2

class Command(BaseCommand):
    help = 'بررسی اتصال به پایگاه داده PostgreSQL'

    def handle(self, *args, **options):
        db_conn = connections['default']
        
        try:
            # تلاش برای اتصال به پایگاه داده
            with db_conn.cursor() as cursor:
                cursor.execute("SELECT 1")
                one = cursor.fetchone()[0]

                if one == 1:
                    self.stdout.write(
                        self.style.SUCCESS('اتصال به PostgreSQL با موفقیت برقرار شد')
                    )
                    
                    # دریافت اطلاعات نسخه PostgreSQL
                    cursor.execute("SELECT version()")
                    version = cursor.fetchone()[0]
                    self.stdout.write(f'نسخه PostgreSQL: {version}')
                    
        except OperationalError as e:
            self.stdout.write(
                self.style.ERROR(f'خطا در اتصال به PostgreSQL: {e}')
            )
        except psycopg2.Error as e:
            self.stdout.write(
                self.style.ERROR(f'خطای Psycopg2: {e}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'خطای ناشناخته: {e}')
            )
