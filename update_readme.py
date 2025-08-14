import os
import requests
import re

def main():
    # Get the GitHub token and organization name from environment variables
    token = os.environ.get("PERSON_TOKEN")
    org_name = os.environ.get("ORG_NAME", "gsmlg-app")

    if not token:
        raise ValueError("PERSON_TOKEN environment variable is not set")

    # Set up the headers for the GitHub API request
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }

    # Get the list of repositories for the organization
    url = f"https://api.github.com/orgs/{org_name}/repos"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    repos = response.json()

    # Generate the markdown table
    table = "| Repository | Language | Stars | Forks |\n"
    table += "|------------|----------|-------|-------|\n"
    for repo in sorted(repos, key=lambda r: r['stargazers_count'], reverse=True):
        name = f"[{repo['name']}]({repo['html_url']})"
        language = repo['language'] or 'N/A'
        stars = repo['stargazers_count']
        forks = repo['forks_count']
        table += f"| {name} | {language} | {stars} | {forks} |\n"

    # Read the README.md file
    readme_path = "profile/README.md"
    with open(readme_path, "r") as f:
        readme_content = f.read()

    # Replace the content between the markers
    start_marker = "<!-- REPO_LIST:START -->"
    end_marker = "<!-- REPO_LIST:END -->"

    # Use a regular expression to replace the content
    # The 's' flag allows '.' to match newlines
    new_content = re.sub(
        f"{start_marker}.*{end_marker}",
        f"{start_marker}\n{table}\n{end_marker}",
        readme_content,
        flags=re.DOTALL,
    )

    # Write the updated content back to the README.md file
    with open(readme_path, "w") as f:
        f.write(new_content)

if __name__ == "__main__":
    main()
