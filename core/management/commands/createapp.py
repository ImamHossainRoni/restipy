from django.core.management.base import BaseCommand
from django.core.management import call_command
import os


class Command(BaseCommand):
    help = 'Creates a new Django app with specific structure'

    def add_arguments(self, parser):
        parser.add_argument('app_name', type=str, help='Name of the new app')

    def handle(self, *args, **kwargs):
        app_name = kwargs['app_name']

        app_dir = os.path.join('apps', app_name)

        os.makedirs(app_dir, exist_ok=True)

        call_command('startapp', app_name, app_dir)

        # Create the dao.py file in the app's directory
        dao_file_path = os.path.join(app_dir, 'dao.py')
        with open(dao_file_path, 'w') as dao_file:
            dao_file.write('# Add your DAO code here\n')
            dao_file.write('\n')

        # Create the service.py file in the app's directory
        service_file_path = os.path.join(app_dir, 'service.py')
        with open(service_file_path, 'w') as service_file:
            service_file.write('# Add your service code here\n')
            service_file.write('\n')

        # Create the urls.py file in the app's directory
        urls_file_path = os.path.join(app_dir, 'urls.py')
        with open(urls_file_path, 'w') as urls_file:
            urls_file.write('from django.urls import path\n\n')
            urls_file.write('# Add your URL patterns here\n')
            urls_file.write('urlpatterns = [\n')
            urls_file.write('    # Add your URL patterns here\n')
            urls_file.write(']\n')

        self.stdout.write(self.style.SUCCESS(f'➡️Successfully created app "{app_name}" within the "apps" directory '
                                             f'with the desired files. 👍'))