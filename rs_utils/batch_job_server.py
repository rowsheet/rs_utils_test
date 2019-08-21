from flask import Flask
from flask import request
import threading
import json
from rs_utils.batch_job import BatchJob
from rs_utils.batch_job_queue import BatchJobQueue
app = Flask(__name__)

class BatchJobServer:

    BATCH_JOB_QUEUE = None
    port = None

    def __init__(self, port=6000):
        self.BATCH_JOB_QUEUE = BatchJobQueue()
        self.port = port

    def run(self):
        @app.route('/')
        def index():
            return self.BATCH_JOB_QUEUE.dump()


        @app.route('/push', methods=["POST"])
        def push():
            json_obj = json.loads(request.data)
            job = BatchJob(
                name=json_obj["NAME"],
            )
            if ("CMD" not in json_obj) and ("EXEC" not in json_obj):
                return "Invalid job: One of EXEC or CMD must be specified."
            if ("CMD" in json_obj) and ("EXEC" in json_obj):
                return "Invalid job: Only one of EXEC or CMD can be specified."
            if "CMD" in json_obj:
                job._cmd = json_obj["CMD"]
            if "EXEC" in json_obj:
                job._exec = json_obj["EXEC"]
            if "NEXT_JOB" in json_obj:
                job.next_job = json_obj["NEXT_JOB"]
            self.BATCH_JOB_QUEUE.add_job(job)
            return "GOT PUSH"

        queue_thread = threading.Thread(target=self.BATCH_JOB_QUEUE.run)
        queue_thread.start()

        app.run(
            host="0.0.0.0",
            port=str(self.port),
        )

if __name__ == "__main__":
    server = BatchJobServer()
    server.run()
