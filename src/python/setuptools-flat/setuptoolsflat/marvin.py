from importlib import resources

def suite_version():
    version = resources.read_text(__package__, "version")
    return version.strip()
