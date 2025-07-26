# Kubernetes PostgreSQL Deployment Project

        This project demonstrates how to deploy an open-source SQL database (PostgreSQL) into a local Kubernetes cluster provided by Docker Desktop, and interact with it using Python.

        ## Learning Objectives Achieved:
        * Enabling and using Docker Desktop's Kubernetes.
        * Creating Kubernetes Deployment, Service, and Persistent Volume Claim manifests.
        * Containerizing an application (PostgreSQL).
        * Connecting to and interacting with a SQL database from Python.
        * Practicing Git for version control and pushing to GitHub.

        ## Project Structure:

        k8s_pg_project/
        +- k8s_manifests/
        |   +- postgres-deployment.yaml
        |   +- postgres-pvc.yaml
        |   `- postgres-service.yaml
        +- src/
        |   `- db_interaction.py
        +- .git/
        +- .gitignore
        `- requirements.txt

        ## Setup and Running the Project:

        ### Prerequisites:
        * Docker Desktop (with Kubernetes enabled) installed and running on Windows.
        * WSL2 (Ubuntu/Debian recommended) installed and configured.
        * Python 3.8+ installed in your WSL environment.
        * Git installed.
        * VS Code installed with Remote - WSL extension.

        ### Steps:

        1.  Clone the Repository (if starting fresh):
            git clone https://github.com/your-username/k8s-postgres-project.git
            cd k8s-postgres-project
            (Skip this if you're continuing from your local development.)

        2.  Open in VS Code (from WSL):
            code .

        3.  Set up Python Virtual Environment:
            python3 -m venv .venv
            source ./.venv/bin/activate
            pip install -r requirements.txt

        4.  Deploy PostgreSQL to Kubernetes:
            Ensure Docker Desktop is running and Kubernetes is enabled.
            kubectl apply -f k8s_manifests/postgres-pvc.yaml
            kubectl apply -f k8s_manifests/postgres-deployment.yaml
            kubectl apply -f k8s_manifests/postgres-service.yaml
            Verify deployment status:
            kubectl get pods -l app=postgres
            kubectl get services -l app=postgres
            Wait until the pod status is Running.

        5.  Interact with the Database:
            python src/db_interaction.py
            This script will connect to the deployed PostgreSQL, create a table, insert some data, and then fetch it.

        6.  Cleanup Kubernetes Resources (Optional):
            kubectl delete -f k8s_manifests/postgres-service.yaml
            kubectl delete -f k8s_manifests/postgres-deployment.yaml
            kubectl delete -f k8s_manifests/postgres-pvc.yaml

        ## Database Details:
        * Host: localhost (from your Windows machine)
        * Port: 30007 (as defined in postgres-service.yaml nodePort)
        * Database Name: mydatabase
        * User: myuser
        * Password: mypassword

        (Remember: For production, use Kubernetes Secrets for sensitive credentials!)

        ## SQL Snippets to Play With:

        To interact directly with the database (e.g., using psql client if installed, or any SQL client):

        -- Connect to the database (replace details as per your setup):
        -- psql -h localhost -p 30007 -d mydatabase -U myuser

        -- List all tables:
        \dt

        -- Describe the 'users' table:
        \d users

        -- Select all data from 'users' table:
        SELECT * FROM users;

        -- Insert another user:
        INSERT INTO users (name, email) VALUES ('Diana Prince', 'diana@example.com');

        -- Update a user's email:
        UPDATE users SET email = 'alice.new@example.com' WHERE name = 'Alice Smith';

        -- Delete a user:
        DELETE FROM users WHERE name = 'Bob Johnson';

        -- Drop the table (be careful!):
        DROP TABLE users;
