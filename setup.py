# -*- coding: utf-8 -*-
"""setup -- setuptools setup file for arl.

$Author: $
$Rev: $
$Date: $
"""

__author__ = "Anylo"
__author_email__ = "anylonen@gmail.com"
__version__ = "0.0.3"
__date__ = "2011-04-01"

try:
    import setuptools
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()

from setuptools import setup, find_packages

__description__ = """Anylo's RogueLike is a simple roguelike game."""

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
