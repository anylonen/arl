# -*- coding: utf-8 -*-
"""setup -- setuptools setup file for arl.

$Author: $
$Rev: $
$Date: $
"""

__author__ = "Anylo76"
__author_email__ = "anylo76@users.sourceforge.net"
__version__ = "0.0.2"
__date__ = "2010-03-01"

try:
    import setuptools
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()

from setuptools import setup, find_packages

__description__ = """Anylo's RogueLike

Anylo's RogueLike is a simple roguelike game.

"""

setup(
    name = "arl",
    version = __version__,
    author = __author__,
    author_email = __author_email__,
    description = __description__,
    url = "http://arl.sourceforge.net",

    packages = find_packages(),

    include_package_data = True,
    zip_safe = False,
    )
