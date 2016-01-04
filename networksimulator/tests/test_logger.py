from networksimulator import logger
import pytest
import os
import shutil


DEFAULT_DIR = os.path.join(os.getcwd(), 'dump')
DEFAULT_FILE_PATH = os.path.join(DEFAULT_DIR, 'log_test.pickle')


@pytest.fixture(scope='module')
def file(request):
    os.makedirs(DEFAULT_DIR, exist_ok=True)

    def fin():
        shutil.rmtree(DEFAULT_DIR)
    request.add_finalizer(fin)

    return open(os.path.join(DEFAULT_FILE_PATH, 'log_test.pickle'), 'ab')


def test_build_logger():
    pass


def test_write_to_file(file):
    pass