from flask import Flask, request, jsonify
from src.pubnub_python_metrics.app.main import create_pubnub_user
#import logging
#from logging.handlers import RotatingFileHandler

# TODO: fix abstract in probable-fiesta
#logger = logging.getLogger(__name__)
#formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
#logger.setLevel(logging.DEBUG)
#handler = RotatingFileHandler('/home/vagrant/opt/python/log/application.log', maxBytes=1024,backupCount=5)
#pathlib.Path('/opt/python/log/application.log').mkdir(parents=True, exist_ok=True)
#handler = RotatingFileHandler('/opt/python/log/application.log', maxBytes=1024,backupCount=5)
#handler = RotatingFileHandler('/var/log/app-logs/application.log', maxBytes=1024,backupCount=5) 
#handler.setFormatter(formatter)

application = Flask(__name__)
#application.logger.addHandler()

@application.route('/v1/metrics/all_metrics', methods=['GET'])
def all_metrics():
    pu = create_pubnub_user()
    return jsonify({'all_metrics': pu.all_metrics()})

# Call me:
#$ curl -i http://127.0.0.1:5000/v1/metrics/get_all_metrics \
#curl -i http://flask-env.eba-nam2bedw.us-east-1.elasticbeanstalk.com \
#-X POST \
#-H 'Content-Type: application/json' \
#-d '{"email":"email","password":"password","start_date":"2020-01-01","end_date":"2020-01-02"}'
@application.post("/v1/metrics/get_all_metrics")
def get_all_metrics():
    if request.is_json:
        pubnub_user_req = request.get_json()
        email = pubnub_user_req["email"]
        password = pubnub_user_req["password"]
        start_date = pubnub_user_req["start_date"]
        end_date = pubnub_user_req["end_date"]
        pu = create_pubnub_user(email=str(email), password=str(password), app=application)
        if pu is None:
            return {"error": "Invalid credentials"}, 401
        return pu.get_all_metrics_by_date(start_date, end_date)
    return {"error": "Request must be JSON"}, 415

if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()