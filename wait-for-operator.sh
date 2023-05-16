
#!/bin/bash
namespace="cp4ba-starter"
while ! echo $(oc get csv -n "$namespace" --no-headers -o custom-columns=NAME:.metadata.name) | grep -c "ibm-cp4a-operator.*";
do
    echo "Waitng for csv to install..."
    sleep 10
done
echo "CSV installed!"
echo "Waiting for operator to be ready..."
cp4baOperator=$(oc get csv -n "$namespace" --no-headers -o custom-columns=NAME:.metadata.name | grep "ibm-cp4a-operator.*")
echo "csv/$cp4baOperator"
while [[ -z $(oc get csv/$cp4baOperator -n "$namespace" -o 'jsonpath={.status.phase}' | grep 'Succeeded') ]]; do
    echo "Waiting for CSV to reach 'Succeeded' condition..."
    sleep 10
done
echo "Done!"