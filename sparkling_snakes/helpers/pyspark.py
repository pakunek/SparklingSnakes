import pyspark

from sparkling_snakes.helpers.app_config import AppConfigHelper


class PySparkHelper:
    def __init__(self, app_config: AppConfigHelper):  # TODO: Cleanup, docs
        self.sc: pyspark.SparkContext = None
        self.config = app_config.get_config()

    def connect_to_cluster(self):  # TODO: Cleanup, docs
        conf = pyspark.SparkConf()
        conf.setMaster(self.config['spark']['master_uri'])
        conf.set('spark.authenticate', False)  # TODO: add at least basic auth in the future
        self.sc = pyspark.SparkContext(conf=conf)

    def test_cluster_operation_primes_from_range(self, range_n: int) -> list[int]:  # TODO: remove
        def is_prime(n):
            for i in range(2, n):
                if (n % i) == 0:
                    return False
            return True

        rdd = self.sc.parallelize(range(range_n), 2)
        return rdd.filter(is_prime).collect()
