from google.cloud import dataproc
from google.api_core.client_options import ClientOptions
from datetime import datetime
from time import sleep
import logging
import os

_REGION = os.environ.get('REGION')
_PROJECT_ID = os.environ.get('PROJECT_ID')
_WORKFLOW_TEMPLATE = os.environ.get('DATAPROC_WORKFLOW')

def _check_execution(execution):
    """Check dataproc workflow execution

    Args:
        execution : Dataproc execution object

    Raises:
        Exception: Except in case job isn't running
    """

    job_running = False
    state_running = 3
    while execution.running() and not job_running:
        job_running = any([job.state == state_running for job in execution.metadata.graph.nodes])
        sleep(2)


def main(request):
    """_summary_

    Args:
        request (http.request): Request to cloud function
    """

    start = datetime.utcnow()
    options = ClientOptions(api_endpoint = f"{_REGION}-dataproc.googleapis.com:443")
    client = dataproc.WorkflowTemplateServiceClient(client_options = options)
    name = client.workflow_template_path(_PROJECT_ID, _REGION, _WORKFLOW_TEMPLATE)

    
    logging.info(f"Starting workflow {_WORKFLOW_TEMPLATE}")
    try:
        execution = client.instantiate_workflow_template(
            name = name,
            parameters = {}
        )       
    
        _check_execution(execution)
        execution.result()  
    except Exception as e:
        raise e

    
    logging.info(f'Workflow {_WORKFLOW_TEMPLATE} started ({datetime.utcnow() - start})')