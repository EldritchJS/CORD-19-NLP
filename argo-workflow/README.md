# CORD-19 NLP Argo Workflow

This .yaml provides a means to perform the following steps, it assumes an exiting OpenShift cluster with a persistent volume large enough for the desired file, with a running Argo workflow server instance:

1. Create data acquisition pod with persistent volume claim 
2. Release PVS
3. Create data process pod with PVC
4. Release PVC

