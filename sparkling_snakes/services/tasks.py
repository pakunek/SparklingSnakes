from sparkling_snakes.api.models.schemas.tasks import TaskInResponse
from sparkling_snakes.helpers.app_config import AppConfigHelper
from sparkling_snakes.helpers.pyspark import PySparkHelper


class TasksService:  # TODO: Cleanup, preferably inject/reuse helpers, split pyspark code from business logic
    @staticmethod
    def run_task(n: int) -> TaskInResponse:
        def is_prime(candidate: int) -> bool:
            for i in range(2, candidate):
                if (candidate % i) == 0:
                    return False
            return True

        config_helper = AppConfigHelper()
        pyspark_helper = PySparkHelper(config_helper.get_config())

        rdd = pyspark_helper.get_context().parallelize(range(n), 2)
        results = rdd.filter(is_prime).collect()

        return TaskInResponse(message=f"Calculations complete, primes for given range are: {results}")
