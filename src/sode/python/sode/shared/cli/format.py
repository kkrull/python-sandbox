from argparse import ArgumentDefaultsHelpFormatter, RawTextHelpFormatter


class DefaultsAndRawTextFormatter(ArgumentDefaultsHelpFormatter, RawTextHelpFormatter):
    """Adds argument defaults and uses pre-formatted text in help"""

    pass
