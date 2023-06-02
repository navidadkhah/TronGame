###############################################################
###                                                         ###
###     Don't forget to set directories in configs.json     ###
###       * set code_base_directory to the address where    ###
###         your whole game folder is.                      ###
###                                                         ###
###############################################################

import os
import threading
import time
import json


configs = json.loads(open(("configs.json"), "r").read())
code_base_directory = configs["code_base_directory"]


class RunServer(threading.Thread):
    def run(self):
        print("Running Server...")
        os.system('cd {}PythonServer && python main.py'.format(code_base_directory))


class RunClient(threading.Thread):
    def run(self):
        print("Running Client...")
        os.system('cd {}PythonClient && python main.py'.format(code_base_directory))


class RunRandomClient(threading.Thread):
    def run(self):
        print("Running Random Client...")
        os.system('cd {}PythonRandomClient && python main.py'.format(code_base_directory))



if __name__ == '__main__':

    run_server = RunServer(name="RunServer")
    run_random_client = RunRandomClient(name="RunRandomClient")
    run_client = RunClient(name="RunClient")

    run_server.start()
    time.sleep(1)
    if configs["run_python_client"]:
        run_client.start()
        time.sleep(1)
    if configs["run_python_random_client"]:
        run_random_client.start()
