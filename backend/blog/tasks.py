# blog/tasks.py
import logging
from django.core.mail import get_connection, EmailMultiAlternatives
from django.contrib.auth.models import User
from celery import shared_task
from .email_templates import NEW_POST_EMAIL_HTML_TEMPLATE
from decouple import config

logger = logging.getLogger(__name__)


def send_mass_html_mail(
    datatuple, fail_silently=False, user=None, password=None, connection=None
):
    """自訂 mass mail，支援 HTML"""
    connection = connection or get_connection(
        username=user, password=password, fail_silently=fail_silently
    )
    messages = []
    for subject, text, html, from_email, recipient in datatuple:
        message = EmailMultiAlternatives(subject, text, from_email, recipient)
        if html:
            message.attach_alternative(html, "text/html")
        messages.append(message)
    return connection.send_messages(messages)


@shared_task
def notify_users_new_post(post_id, title, url):
    users = User.objects.all().values_list("email", flat=True)
    subject = f"新文章發布：{title}"

    text_message = f"{config('WEBSITE_TITLE')}剛發了新文章:\n\n{title}\n\n閱讀完整內容：{url}\n\nEmail: {config('GOOGLE_EMAIL_USER')}\nBlog: {config('FRONTEND_URL')}"

    html_content = NEW_POST_EMAIL_HTML_TEMPLATE.format(
        post_sender=config("WEBSITE_TITLE"),
        post_title=title,
        post_url=url,
        post_sender_email=config("GOOGLE_EMAIL_USER"),
        FRONTEND_URL=config("FRONTEND_URL"),
    )

    datatuple = [
        (subject, text_message, html_content, config("GOOGLE_EMAIL_USER"), [email])
        for email in users
        if email
    ]

    logger.info(f"[Post #{post_id}] 寄送通知給 {len(datatuple)} 位用戶")

    if datatuple:
        try:
            send_mass_html_mail(datatuple, fail_silently=False)
            logger.info("通知信寄出成功")
        except Exception as e:
            logger.error(f"通知信寄送失敗: {e}")
