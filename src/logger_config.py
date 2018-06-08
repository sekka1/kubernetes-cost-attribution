import logging

FORMAT = "\n%(asctime)s - %(levelname)s - pod_usage=1.0, %(message)s"
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

def configure_logger(logger, filename=None):
  # logger.setLevel(logging.INFO)
  logger.setLevel(logging.DEBUG)

  if filename is None:
      handler = logging.StreamHandler()
  else:
      handler = logging.FileHandler(filename)

#  handler.setLevel(logging.DEBUG)

  formatter = logging.Formatter(fmt=FORMAT, datefmt=DATE_FORMAT)
  handler.setFormatter(formatter)
  logger.addHandler(handler)

  return logger

logging.captureWarnings(True)

logger = logging.getLogger()
logger = configure_logger(logger)
