from app import create_app, db
from app.models import User
from app.utils.password_utils import hash_password

DEFAULTS = [
    ("admin", "admin123", "admin"),
    ("manager", "manager123", "manager"),
    ("engineer", "engineer123", "engineer"),
    ("operator", "operator123", "operator"),
]

def run_seed():
    app = create_app()
    with app.app_context():
        for username, pwd, role in DEFAULTS:
            if not User.query.filter_by(username=username).first():
                u = User(username=username, password_hash=hash_password(pwd), role=role)
                db.session.add(u)
                print(f"Seeded {role}: {username}/{pwd}")
        db.session.commit()

if __name__ == "__main__":
    run_seed()
