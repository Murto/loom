import sys, os

LOOM_PATH = '../loom'
TEST_PATH = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath(os.path.join(TEST_PATH, LOOM_PATH)))
