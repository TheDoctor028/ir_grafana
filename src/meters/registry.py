from prometheus_client import CollectorRegistry

registry = CollectorRegistry()


def get_job_name() -> str:
    return 'iracing_telemetry_client'
