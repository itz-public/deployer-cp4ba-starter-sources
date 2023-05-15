import subprocess, requests, yaml, sys, shutil, os

url = 'https://raw.githubusercontent.com/IBM/cloud-pak/master/repo/case/ibm-cp-automation/index.yaml'
response = requests.get(url)
yaml_content = response.text
requestedVersion = sys.argv[1]
# Parse YAML and extract latest app versions
data = yaml.safe_load(yaml_content)
app_versions = []

index = 0
downloadVersion = ""
for version in data['versions']:
     cp4baVersion = data['versions'][version]['appVersion']
     if requestedVersion in cp4baVersion:
         downloadVersion = version
         
url = "https://github.com/IBM/cloud-pak/raw/master/repo/case/ibm-cp-automation/{}/ibm-cp-automation-{}.tgz".format(
     downloadVersion, downloadVersion)
target_path = "ibm-cp-automation-{}.tgz".format(downloadVersion)
response = requests.get(url, stream=True)
if response.status_code == 200:
    with open(target_path, 'wb') as f:
        f.write(response.raw.read())
cwd = os.getcwd()
subprocess.run(["tar", "-xvzf", target_path, "-C", cwd],
               stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
crsLocation = cwd + "/ibm-cp-automation/inventory/cp4aOperatorSdk/files/deploy/crs/"
dir_list = os.listdir(crsLocation)
fileName = dir_list[0]
subprocess.run(["tar", "-xvf", crsLocation + fileName],
               stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
shutil.copyfile(
    cwd + "/cert-kubernetes/descriptors/op-olm/catalog_source.yaml", "source.yaml")