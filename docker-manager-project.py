import sys
import docker

def run_docker(repo_url):
    client = docker.from_env()
    container = client.containers.run(
        'pure-js-docker',
        command=repo_url,
        detach=True,
        ports={'8000/tcp': 8000},
        name='web-project-container'
    )

    print(f"Container {container.name} is running. Access the website at http://localhost:8000")

def main(repo_url):
    run_docker(repo_url)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python docker-manager-project.py <github_repo_url>")
        sys.exit(1)
    
    repo_url = sys.argv[1]
    main(repo_url)