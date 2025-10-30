# blog/email_templates.py
NEW_POST_EMAIL_HTML_TEMPLATE = """
<p>{post_sender} 剛發了新文章 :</p>

<h2><a href="{post_url}">{post_title}</a></h2>

<hr>

<p>Email: {post_sender_email}<br>
Blog: <a href="{FRONTEND_URL}">{FRONTEND_URL}</a></p>
"""
