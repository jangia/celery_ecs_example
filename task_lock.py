import datetime
import os
from functools import wraps

from redis.client import Redis

redis = Redis.from_url(os.getenv("REDIS_URL"))
TIME_TO_LIVE = datetime.timedelta(minutes=15).total_seconds()


def lock(job_id):
    success = redis.setnx(
        name=job_id,
        value=job_id,
    )
    if success:
        # There's no way to set key only if it's not there yet, get information whether it was set or not,
        # and set expire time with Python library
        # .set() has all the arguments but returns None in both cases
        redis.expire(name=job_id, time=int(TIME_TO_LIVE))
        return True

    return False


def release(job_id):
    redis.delete(job_id)


def no_parallel_processing_of_task(fun):  # type: ignore
    @wraps(fun)
    def outer(self, *args, **kwargs):  # type: ignore
        try:
            if not lock(job_id=self.request.id):
                self.apply_async(
                    *args,
                    kwargs={**kwargs},
                    countdown=datetime.timedelta(minutes=1).total_seconds(),
                )
                return "Same job is being processed by some other worker"
            result = fun(self, *args, **kwargs)
            release(job_id=self.request.id)
        except Exception as exc:
            release(job_id=self.request.id)
            raise exc
        return result

    return outer
