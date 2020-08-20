# CORD-19-NLP

On an OpenShift cluster you are logged into, create a project if you haven't already, for sake of example we'll call it cord-19

`oc new-project cord-19`

Then load the buildconfig and imagestream information for the acquisition and processing applications via the following:

`oc apply -f cord-19-resources.yaml`

Finally, head over to your Argo workflow webui, click Submit New Workflow, and copy paste what's found in `argo-workflow/workflow.yaml`into the textarea that appears. (Note: change `<PROJECT_NAME>` to your project's name, and delete all the sample YAML that Argo provides.

Click Submit and watch the workflow happen.

