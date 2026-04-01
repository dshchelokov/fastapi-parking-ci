from app import create_app

app = create_app()


def run() -> None:
    app.run(debug=True)


if __name__ == '__main__':
    run()
