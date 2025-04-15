def log_user_object(user_obj):
    # Filter out SQLAlchemy internal attributes (those starting with '_')
    user_dict = {k: v for k, v in user_obj.__dict__.items() if not k.startswith('_')}
    print(f"User data: {user_dict}")  # or use your logger instead of print