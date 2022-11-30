from typing import Any, Optional
import pyspark


class PySparkHelper:
    _instance: Optional['PySparkHelper'] = None
    _config: Optional[dict[str, Any]] = None
    _sc: Optional[pyspark.SparkContext] = None

    def __new__(cls, app_config: dict[str, Any]) -> 'PySparkHelper':
        """Ensure Singleton properties."""
        if cls._instance is None:
            cls._instance = super(PySparkHelper, cls).__new__(cls)
            cls._instance._config = app_config
            cls.get_context()
        return cls._instance

    @classmethod
    def get_context(cls) -> pyspark.SparkContext:  # TODO: Cleanup
        """Connect to config-determined PySpark cluster.

        :return: PySpark context
        """
        if cls._instance._sc is None:
            conf: pyspark.SparkConf = pyspark.SparkConf()
            conf.setMaster(cls._instance._config['spark']['master_uri'])
            conf.set('spark.authenticate', False)  # TODO: add at least basic auth in the future
            cls._instance._sc = pyspark.SparkContext(conf=conf)
        return cls._instance._sc
