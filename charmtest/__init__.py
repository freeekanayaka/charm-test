import platform

from .testing import CharmTest

# XXX Force 'ubuntu' as platform, since charmhelpers.core.host doesn't like
# 'debian' (which is what you get on Travis).
platform.linux_distribution = lambda: ('Ubuntu', '16.04', 'xenial')


__all__ = [
    "CharmTest",
]
