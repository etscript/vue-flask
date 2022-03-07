from app.factory import create_app, db

app = create_app(config_name="PRODUCTION")
app.app_context().push()

@app.teardown_request
def teardown_request(exception):
    if exception:
        db.session.rollback()
    db.session.remove()