def send_verification_email(user, token):
    link = f'http://localhost:5000/verify/{token}'
    print(f'\n===== 验证邮件 =====')
    print(f'收件人: {user.email}')
    print(f'验证链接: {link}')
    print(f'====================\n')


def send_reset_email(user, token):
    link = f'http://localhost:5000/reset-password?token={token}'
    print(f'\n===== 密码重置邮件 =====')
    print(f'收件人: {user.email}')
    print(f'重置链接: {link}')
    print(f'========================\n')
