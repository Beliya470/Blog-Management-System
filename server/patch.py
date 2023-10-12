def apply_patch():
    try:
        import flask_sqlalchemy
        delattr(flask_sqlalchemy.SQLAlchemy, '_include_sqlalchemy')
    except Exception as e:
        print(f"Failed to apply patch: {e}")
