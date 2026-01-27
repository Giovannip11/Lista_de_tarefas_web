from app import create_app, db

app = create_app()

with app.app_context():
    db.create_all()


if __name__ == "main":
    app.run(debug=True)
