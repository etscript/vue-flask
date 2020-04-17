from app.api import bp

@bp.route('/get_testapi', methods=['GET'])
def get_testapi():
    return "testapi"


