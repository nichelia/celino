from diagrams import Cluster, Diagram
from diagrams.programming.framework import Angular
from diagrams.programming.language import Python
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.monitoring import Prometheus, Grafana


def generate_overview_diagram():
    with Diagram("Overview", show=False, filename="bin/overview"):

        with Cluster("Client"):
            webapp =  Angular("webapp")

        with Cluster("API Services"):
            status_service = Python("status_service")
            task_service = Python("task_service")
            worker_service = Python("worker_service")
            metrics_service = Python("metrics_service")

        with Cluster("Intermediate Services"):
            
            with Cluster("Clearly Client Cluster"):
                clearly_client = Python("clearly_client")

        with Cluster("Backend Services"):

            with Cluster("Clearly Server Cluster"):
                clearly_server = Python("clearly_server")

        with Cluster("External Connections"):

            with Cluster("Message Broker"):
                redis = Redis("redis")

            with Cluster("Monitoring"):
                grafana = Grafana("grafana")
                prometheus = Prometheus("prometheus")
        
        
        webapp >> status_service << clearly_client
        webapp >> task_service << clearly_client
        webapp >> worker_service << clearly_client

        clearly_client >> clearly_server >> redis
        metrics_service << prometheus
        metrics_service >> clearly_server


def main():
    generate_overview_diagram()


if __name__ == "__main__":
    main()