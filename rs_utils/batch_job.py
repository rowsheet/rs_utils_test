from rs_utils import logger
from rs_utils import runner
from rs_utils.response import Response
from multiprocessing.pool import ThreadPool

class BatchJob:

    name = None
    _cmd = None
    _exec = None

    status = "created"
    async_result = None

    next_job = None
    prev_job = None

    cleanup = False

    def __init__(self, name=None):
        self.name = name

    def _run_cmd(self):
        def run():
            if type(self._cmd).__name__ == "list":
                self._cmd = " && ".join(self._cmd)
            return runner.step(
                self._cmd,
                self.name,
            )
        pool = ThreadPool(processes=1)
        self.async_result = pool.apply_async(run)

    def _run_exec(self):
        def run():
            try:
                if type(self._exec).__name__ == "list":
                    exec("\n".join(self._exec))
                    return locals()["_response"]
                exec(self._exec)
                return locals()["_response"]
            except Exception as ex:
                response = Response()
                response.ERROR = True
                response.STDOUT = str(ex)
                return response
        pool = ThreadPool(processes=1)
        self.async_result = pool.apply_async(run)

    def start(self):
        logger.debug("JOB START: '%s'" % self.name)
        self.status = "started"
        if self._exec is not None:
            self._run_exec()
        elif self._cmd is not None:
            self._run_cmd()
        else:
            raise Exception("Invalid job. CMD and EXEC are None.")

    def check_done(self):
        if self.async_result is not None:
            if self.async_result.ready() == True:
                response = self.async_result.get()
                if response.ERROR == True:
                    raise Exception(response.STDERR)
                self.status = "done"
