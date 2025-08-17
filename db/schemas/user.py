def user_schema(user)-> dict:
    return {'id': str(user.get('_id')), 
            'username': user.get('username'),
            'email': user.get('email')}

def users_schema(users) -> list:
    return [user_schema(user) for user in users]