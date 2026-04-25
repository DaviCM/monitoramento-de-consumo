import os
from datetime import datetime, timezone
import logging

from dotenv import load_dotenv
from resend.exceptions import ResendError
import resend

from src.models.user_model import User
from src.templates.template_engine import render_template

logger = logging.getLogger(__name__)

load_dotenv()

resend.api_key = os.getenv('RESEND_API_KEY')

def send_recovery_email(target_user: User, recovery_token: str):
    try:
        recovery_html = render_template(template_name='password_recovery_page.html', 
                                        params={'user_real_name': target_user.real_name,
                                                'recovery_url': f'{os.getenv('WEB_APP_URL')}/reset-password?recovery_token={recovery_token}'
                                                })

        email_params: resend.Emails.SendParams = {
            'from': f'{os.getenv('SENDER_NAME')} <{os.getenv('SENDER_ADDRESS')}>',
            'to': target_user.email,
            'subject': 'Pedido de recuperação de senha do Liqua Monitor',
            
            'html': recovery_html
        }

        resp = resend.Emails.send(params=email_params)
        logger.info(f'Recovery e-mail sent at {datetime.now(tz=timezone.utc)}',
                    extra=f'User: {target_user.real_name}, User ID: {target_user.id}, Email ID: {resp.id}'
                    )
    except ResendError as e:
        logger.error(f'Error while sending recovery e-mail at {datetime.now(tz=timezone.utc)}',
                     extra=str(e)
                     )


