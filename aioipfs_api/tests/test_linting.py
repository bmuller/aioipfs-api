import unittest
from glob import glob

import pycodestyle

from pylint import epylint as lint


class LintError(Exception):
    pass


class TestCodeLinting(unittest.TestCase):
    # pylint: disable=no-self-use
    def test_pylint(self):
        (stdout, _) = lint.py_run('aioipfs_api', return_std=True)
        errors = stdout.read()
        if errors.strip():
            raise LintError(errors)

    # pylint: disable=no-self-use
    def test_pep8(self):
        style = pycodestyle.StyleGuide()
        files = glob('aioipfs_api/**/*.py', recursive=True)
        files = [f for f in files if 'autoapi.py' not in f]
        result = style.check_files(files)
        if result.total_errors > 0:
            raise LintError("Code style errors found.")
