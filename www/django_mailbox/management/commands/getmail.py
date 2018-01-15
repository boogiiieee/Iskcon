import logging

from django.core.management.base import BaseCommand

from django_mailbox.models import Mailbox


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class Command(BaseCommand):
    def handle(self, *args, **options):
        mailboxes = Mailbox.objects.filter(active=True)
        
        if args:
            mailboxes = mailboxes.filter(
                name=' '.join(args)
            )
        for mailbox in mailboxes:
            logger.info(
                'Gathering messages for %s',
                mailbox.name
            )
            try:
                messages = mailbox.get_new_mail()
                for message in messages:
                    logger.info(
                        'Received %s (from %s)',
                        message.subject,
                        message.from_address
                    )
            except:
                logger.info('Error receive.')
