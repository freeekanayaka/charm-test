import platform

from testtools import try_import

from .fixture import CharmFakes
from .testing import CharmTest

# XXX Force 'ubuntu' as platform, since charmhelpers.core.host doesn't like
# 'debian' (which is what you get on Travis).
platform.linux_distribution = lambda: ('Ubuntu', '16.04', 'xenial')

# XXX Force systemd as init system, since Travis doesn't yet support xenial.
host = try_import("charmhelpers.core.host")

if host:
    host.init_is_systemd = lambda: True


__all__ = [
    "CharmFakes",
    "CharmTest",
]
