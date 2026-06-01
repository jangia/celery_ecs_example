import datetime
import os
from functools import wraps

from redis.client import Redis

redis = Redis.from_url(os.getenv("REDIS_URL"))
TIME_TO_LIVE = datetime.timedelta(minutes=15).total_seconds()


class LockNotAcquired(Exception):
    pass


def lock(job_id):
    return bool(redis.set(name=job_id, value=job_id, nx=True, ex=int(TIME_TO_LIVE)))


def release(job_id):
    redis.delete(job_id)


def no_parallel_processing_of_task(fun):  # type: ignore
    @wraps(fun)
    def outer(self, *args, **kwargs):  # type: ignore
        acquired = lock(job_id=self.request.id)
        if not acquired:
            raise LockNotAcquired(
                f"Task {self.request.id} is already being processed by another worker"
            )
        try:
            return fun(self, *args, **kwargs)
        finally:
            if acquired:
                release(job_id=self.request.id)

    return outer
