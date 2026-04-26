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
        logger.info(f'E=mail de recuperação de senha enviado às {datetime.now(tz=timezone.utc)} UTC',
                    extra=f'Usuário: {target_user.real_name}, ID: {target_user.id}, E-mail ID: {resp.id}'
                    )
        
    except ResendError as e:
        logger.error(f'Erro ao enviar e=mail de recuperação às {datetime.now(tz=timezone.utc)} UTC',
                     extra=str(e)
                     )


