"""
This script configures git for code signing.

I often reinstall my Arch Linux or Windows, and then I forget to set it up, so I just make
this script so that I can't forget it anymore.


"""


import os
import subprocess


def configure_git_signing(gpg_key_id):
    # Configure Git to use the specific GPG key for signing commits
    subprocess.run(['git', 'config', '--global', 'user.signingkey', gpg_key_id], check=True)
    subprocess.run(['git', 'config', '--global', 'commit.gpgSign', 'true'], check=True)


def create_pre_commit_hook(repo_path, gpg_key_id):
    pre_commit_hook_path = os.path.join(repo_path, '.git', 'hooks', 'pre-commit')
    hook_content = f"""#!/bin/sh

# Ensure the commit is signed
if ! git log -1 --pretty=%G? | grep -q 'G'; then
  echo "Error: Commit is not signed."
  exit 1
fi

# Verify the commit is signed with the specific key
KEY_ID="{gpg_key_id}"
if ! git log -1 --pretty=%GK | grep -q "$KEY_ID"; then
  echo "Error: Commit is not signed with the required key: $KEY_ID."
  exit 1
fi
"""

    with open(pre_commit_hook_path, 'w') as hook_file:
        hook_file.write(hook_content)

    os.chmod(pre_commit_hook_path, 0o755)


def create_server_side_hook(repo_path, gpg_key_id):
    pre_receive_hook_path = os.path.join(repo_path, 'hooks', 'pre-receive')
    hook_content = f"""#!/bin/sh

KEY_ID="{gpg_key_id}"

while read oldrev newrev refname; do
  # Check all commits in the pushed ref
  for commit in $(git rev-list ${{oldrev}}..${{newrev}}); do
    # Ensure the commit is signed
    if ! git cat-file commit ${{commit}} | grep -q '^gpgsig'; then
      echo "Error: Commit ${{commit}} is not signed."
      exit 1
    fi

    # Verify the commit is signed with the specific key
    if ! git log -1 --pretty=%GK ${{commit}} | grep -q "$KEY_ID"; then
      echo "Error: Commit ${{commit}} is not signed with the required key: $KEY_ID."
      exit 1
    fi
  done
done
"""

    with open(pre_receive_hook_path, 'w') as hook_file:
        hook_file.write(hook_content)

    os.chmod(pre_receive_hook_path, 0o755)


def main():
    gpg_key_id = "1E04D0A679846BC0"
    repos_file = "repositories.txt".strip()

    if not os.path.isfile(repos_file):
        print("Invalid file path")
        return

    with open(repos_file, 'r') as file:
        repo_paths = [line.strip() for line in file if line.strip()]

    configure_git_signing(gpg_key_id)

    for repo_path in repo_paths:
        if os.path.isdir(repo_path):
            create_pre_commit_hook(repo_path, gpg_key_id)
        else:
            print(f"Invalid repository path: {repo_path}")

    create_server_side = input("Do you want to create a server-side hook? (yes/no): ").strip().lower()
    if create_server_side == 'yes':
        server_repo_path = input("Enter the path to the server-side repository: ").strip()
        create_server_side_hook(server_repo_path, gpg_key_id)

    print("Configuration complete.")

if __name__ == "__main__":
    main()