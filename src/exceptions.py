"""
Exception classes used in the sample runner.
"""


class AccountStateError(Exception):
    "For when an account doesn't have the right preconditions to support a sample."
    pass
