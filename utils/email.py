def send_verification_email(user, token):
    """发送账号验证邮件（项目用户注册验证）

    Args:
        user: 用户对象，包含email等信息
        token: 验证令牌，用于生成验证链接
    """
    link = f'http://localhost:5000/verify/{token}'
    print('\n===== 验证邮件 =====')
    print(f'收件人：{user.email}')
    print(f'验证链接：{link}')
    print('====================\n')


def send_reset_email(user, token):
    """发送密码重置邮件（项目用户密码找回）

    Args:
        user: 用户对象，包含email等信息
        token: 重置令牌，用于生成重置链接
    """
    link = f'http://localhost:5000/reset/{token}'
    print('\n===== 密码重置邮件 =====')
    print(f'收件人：{user.email}')
    print(f'重置链接：{link}')
    print('========================\n')
