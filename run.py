from app.factory import create_app, celery_app

app = create_app(config_name="DEVELOPMENT")
app.app_context().push()

def after_request(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

app.after_request(after_request)

if __name__ == "__main__":
   app.run(port=5000)
