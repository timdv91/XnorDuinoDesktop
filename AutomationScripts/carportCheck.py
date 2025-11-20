import requests
import subprocess
import os


class requestTest():
    def __init__(self, pURL):
        self.URL = pURL

    def get(self, pData, pPath=""):
        # GET request:
        r = requests.get(str(self.URL + "/" + pPath), data=(pData))
        return r.text

    def post(self, pData, pPath=""):
        # POST request:
        r = requests.post(str(self.URL + "/" + pPath), data=(pData))
        return r.text


REMOTE_DEV = "xxxxxxxxxxxxxxxxx"
lockf_path = "/tmp/carportClosed.lock"

reqT = requestTest('xxxxxxxxxxxxxxxxxx')
value = reqT.get('["' + REMOTE_DEV + '","get_dio_value()","IOLine.DIO2_AD2"]', "R")

if value == "IOValue.HIGH":
    if os.path.exists(lockf_path) == False:
        subprocess.run(["bash", "ssh-carport-webhook.sh", "false"], check=True)     # Carport closed
        with open(lockf_path, "w") as f:
            f.write(str(os.getpid()))
        print("Closed webhook call has been send, lockfile is put in place.")
    else:
        print("No webhook call required, close message already send.")
else:
    subprocess.run(["bash", "ssh-carport-webhook.sh", "true"], check=True)      # Carport opened
    if os.path.exists(lockf_path):
        os.remove(lockf_path)
    print("Open webhook call has been send, lockfile has been removed.")