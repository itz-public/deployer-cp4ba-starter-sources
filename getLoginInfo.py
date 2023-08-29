import os
import subprocess
import json


namespace = os.environ.get("NAMESPACE")
configmap_name = "icp4adeploy-cp4ba-access-info"
command = f"oc get configmap/{configmap_name} -n {namespace} -o" + "jsonpath='{.data}'"
process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
stdout, stderr = process.communicate()
if process.returncode == 0:
    # ConfigMap successfully retrieved
    value = stdout.decode("utf-8")
    configMapValues = json.loads(value)
    for configMapValue in configMapValues:
        print(configMapValue)
        print(configMapValues[configMapValue])
        print("=================")
else:
    # Error occurred while executing the command
    print(f"Error executing command: {stderr.decode('utf-8')}")
