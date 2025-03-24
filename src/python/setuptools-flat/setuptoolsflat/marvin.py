from importlib import resources

def suite_version():
    return resources.read_text(__package__, "version")
