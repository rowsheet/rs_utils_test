from rs_utils import logger
import traceback
import json

class BatchJobQueue:

    jobs = {}

    """
    Track jobs with next_job attribute and mark down their name keyed by
    their next_job so that we can look up jobs as they come in. If their
    name is a key in next_job_names_tracking, their prev_job will be the
    job that has that job as it's next_job.
    """
    next_job_names_tracking = {}

    def add_job(self, job):
        if job.name in self.next_job_names_tracking:
            job.prev_job = self.next_job_names_tracking[job.name]
        if job.next_job is not None:
            self.next_job_names_tracking[job.next_job] = job.name
        self.jobs[job.name] = job

    def dump(self):
        job_dict = {}
        for job_name, job in self.jobs.items():
            job_log = {
                "name": job.name,
                "status": job.status,
                "cmd": job._cmd,
            }
            if job.async_result is not None:
                job_log["async_ready"] = job.async_result.ready()
            else:
                job_log["async_ready"] = False
            if job.next_job is not None:
                job_log["next_job"] = job.next_job
            if job.prev_job is not None:
                job_log["prev_job"] = job.prev_job
            job_log["cleanup"] = job.cleanup
            job_dict[job_name] = job_log
        dump = json.dumps(job_dict, indent=4)
        return dump

    """
    Jobs may have a NEXT_JOB. If a job has a NEXT_JOB, that job may 
    also have a NEXT_JOB. Recursivly check all self.jobs to check 
    if all jobs are loaded.
    """
    def _validate_job_chain_loaded(self, job_name):
        if job_name not in self.jobs:
            return False
        job = self.jobs[job_name]
        if job.next_job is not None:
            return self._validate_job_chain_loaded(job.next_job)
        return True

    def _validate_prev_job_chain_done(self, job_name):
        job = self.jobs[job_name]
        if job.prev_job is None:
            return True
        prev_job = self.jobs[job.prev_job]
        if prev_job.status == "done":
            return True
        return False

    def _validate_next_job_chain_done(self, job_name):
        job = self.jobs[job_name]
        if job.next_job is None:
            if job.status == "done":
                return True
            return False
        next_job = self.jobs[job.next_job]
        if next_job.status == "done":
            self._validate_next_job_chain_done(next_job.name)
        return False

    def _mark_next_chain_for_cleanup(self, job):
        job.cleanup = True
        if job.next_job is not None:
            if job.next_job in self.jobs:
                next_job = self.jobs[job.next_job]
                self._mark_next_chain_for_cleanup(next_job)

    def _mark_prev_chain_for_cleanup(self, job):
        job.cleanup = True
        if job.prev_job is not None:
            if job.prev_job in self.jobs:
                prev_job = self.jobs[job.prev_job]
                self._mark_prev_chain_for_cleanup(prev_job)

    def _mark_job_chain_for_cleanup(self, job):
        job.cleanup = True
        self._mark_prev_chain_for_cleanup(job)
        self._mark_next_chain_for_cleanup(job)

    def _safe_eval_job(self, job_name):
        try:
            job = self.jobs[job_name]
            if job.cleanup == True:
                logger.warning(job_name + " cleanup True, skipping...")
                return
            job.check_done()
            if job.status == "created":
                if self._validate_job_chain_loaded(job_name) == True:
                    if self._validate_prev_job_chain_done(job_name) == True:
                        job.start()
            if job.status == "done":
                if self._validate_next_job_chain_done(job_name) == True:
                    self._mark_job_chain_for_cleanup(job)
        except Exception as ex:
            logger.error("JOB ERROR: " + str(ex))
            traceback.print_exc()
            job = self.jobs[job_name]
            self._mark_job_chain_for_cleanup(job)

    def run(self):
        logger.debug("BATCH_JOB_QUEUE START:")
        while True:
            job_names = list(self.jobs)
            for job_name in job_names:
                job = self.jobs[job_name]
                if job.cleanup == True:
                    self.jobs.pop(job_name)
            job_names = list(self.jobs)
            for job_name in job_names:
                self._safe_eval_job(job_name)
