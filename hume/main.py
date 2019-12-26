import multiprocessing
from app_manager import app_manager


if __name__ == '__main__':
    multiprocessing.set_start_method('spawn')
    app_manager.initiate()
