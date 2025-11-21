#!/usr/bin/python


from pathlib import Path
import sys

modulesPath = f"{Path(__file__).resolve().parent}/bin"
sys.path.insert(0, modulesPath)

from soc import Server_soc, Client_soc

server = Server_soc()
Client = Client_soc()

def main():
    # do main
    pass


main()
