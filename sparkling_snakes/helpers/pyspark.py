from typing import Optional

import pyspark
from pyspark import sql

from sparkling_snakes.processor.types import Config


class PySparkHelper:
    """PySpark connection helper class."""

    _instance: Optional['PySparkHelper'] = None
    _config: Optional[Config] = None
    _ss: Optional[pyspark.sql.SparkSession] = None

    def __new__(cls, app_config: Config) -> 'PySparkHelper':
        """Ensure Singleton properties."""
        if cls._instance is None:
            cls._instance = super(PySparkHelper, cls).__new__(cls)
            cls._instance._config = app_config
            cls._instance._ss = None
            cls.get_session()
        return cls._instance

    @classmethod
    def get_session(cls) -> sql.SparkSession:
        """Connect to config-determined PySpark cluster.

        :return: PySpark Session
        """
        if cls._instance._ss is None:
            conf: pyspark.SparkConf = pyspark.SparkConf()
            conf.setMaster(cls._instance._config['spark']['master_uri'])
            conf.set('spark.authenticate', 'false')  # TODO: add at least basic auth in the future
            cls._instance._ss = sql.SparkSession.builder.appName('sparkling_snakes_processor').getOrCreate()
        return cls._instance._ss
