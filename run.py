from app import create_app, database

app = create_app()

@app.cli.command()
def init_db():
    with app.app_context():
        database.create_all()
    print("Tables created!")

if __name__ == '__main__':
    with app.app_context():
        database.create_all()
    app.run(debug=True)