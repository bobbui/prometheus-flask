import random

from flask.globals import request

if __name__ == '__main__':
    import datetime
    import os

    from prometheus_client import Counter, Gauge

    from prometheus.flask import monitor
    from flask import Flask

    categories = ["organism", "being", "benthos", "heterotroph", "cell", "person", "individual", "someone", "somebody",
                  "mortal", "soul", "animal", "animate being", "beast", "brute", "creature", "fauna", "plant", "flora",
                  "plant life", "food", "nutrient", "artifact", "artefact", "hop", "check-in", "dressage", "curvet",
                  "vaulting", "piaffe", "funambulism", "tightrope walking", "rock climbing", "contact sport",
                  "outdoor sport", "field sport", "gymnastics", "gymnastic exercise", "acrobatics", "tumbling",
                  "track and field", "track", "running", "jumping", "broad jump", "long jump", "high jump",
                  "Fosbury flop",
                  "skiing", "cross-country skiing", "ski jumping", "water sport", "aquatics", "swimming", "swim",
                  "bathe",
                  "dip", "plunge", "dive", "diving", "floating", "natation", "dead-man's float", "prone float",
                  "belly flop", "belly flopper", "be"]

    # custom metrics
    # FLASK_CONCURRENT_PROCESSING_QUEUE = Gauge('flask_concurrent_processing_queue', 'Flask Concurrent Processing Queue')
    # FLASK_CONCURRENT_PROCESSING_QUEUE.set_function(lambda: random.randint(0, 5))
    # FLASK_CATEGORIES = Counter("flask_categories", "Categories Counter", ["category"])

    app = Flask(__name__)
    monitor(app)


    def before_request():
        print(request.headers)
        pass


    def after_request(response):
        # FLASK_CATEGORIES.labels(categories[random.randint(0, len(categories) - 1)]).inc()
        return response


    app.before_request(before_request)
    app.after_request(after_request)


    @app.route('/')
    def index():
        print(" --- incoming request --- %s", datetime.datetime.now())
        environ = os.environ
        output = ""
        for env in environ:
            output += env + " : " + environ[env] + "<br>"
        return output


    @app.route('/sync')
    def sync():
        print(" --- incoming sync request --- %s", datetime.datetime.now())
        return "Hello sync"


    @app.route('/async')
    def async():
        print(" --- incoming async request --- %s", datetime.datetime.now())
        return "Hello async"


    # Run the application!
    port = os.getenv('PORT', '5001')
    app.run(port=port, host='0.0.0.0', threaded=True, use_reloader=False)
