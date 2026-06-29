import subprocess
import shutil
import os
from pathlib import Path

REPO_NAME = '{{ cookiecutter.project_repo_name }}'
ORG_NAME = '{{ cookiecutter.project_org }}'
VISIBILITY = '{{cookiecutter.project_visibility}}'
DESCRIPTION = '{{cookiecutter.project_description}}'
LICENSE_ID = '{{cookiecutter.license}}'
PROJECT_TYPE = '{{cookiecutter.project_type}}'
CREATE_REPO = '{{cookiecutter.create_repo}}'
RECEIVE_UPDATES = '{{cookiecutter.receive_updates}}'
ADD_TEAM = '{{cookiecutter.add_team}}'

def createGithubRepo():
    gh_cli_command = [
        "gh", "repo", "create",
        f"{ORG_NAME}/{REPO_NAME}",
        "--source=.",
        f"--{VISIBILITY}",
        "--push",
        f"--description={DESCRIPTION}",
    ]
    subprocess.call(gh_cli_command)
    subprocess.call(["git", "push", "--set-upstream", "origin", "main"])

def addTopic():
    gh_cli_command = [
        "gh", "repo", "edit",
        f"{ORG_NAME}/{REPO_NAME}",
        "--add-topic=dpg-tier0",
    ]
    subprocess.call(gh_cli_command)

def addTeam():
    team = []
    add_member = True
    while add_member:
        member = {}
        member["role"] = input("Project Member's Role (Engineer, Project Lead, COR, etc...): ").strip()
        member["name"] = input("Project Member's Name: ").strip()
        member["affiliation"] = input("Project Member's Affiliation (DSAC, CCSQ, CMMI, etc...): ").strip()
        team.append(member)

        while True:
            add_member_input = input("Would you like to add another project member? [Y/n]: ").strip().lower()
            if add_member_input in ("y", "yes", ""):
                add_member = True
                break
            elif add_member_input in ("n", "no"):
                add_member = False
                break
            else:
                print("\nInvalid response, please respond with: 'y', 'yes', 'n', 'no', or just press Enter for yes")

    team_table = ""
    for member in team:
        team_table += f"""| {member["role"]} | {member["name"]} | {member["affiliation"]} |\n"""

    community_file_path = f"COMMUNITY.md"

    with open(community_file_path, "r") as f:
        lines = f.readlines()

    with open(community_file_path, "w") as f:
        for line in lines:
            if "| {role} | {names} | {affiliations} |" in line:
                f.write(team_table)  # Replace placeholder line with new table of project team members
            else:
                f.write(line)

def moveCookiecutterFile(): 
    original_dir = os.getcwd()

    try:
        github_dir = os.path.join(original_dir, ".github")
        os.chdir(github_dir)
        Path("./codejson").mkdir(parents=True, exist_ok=True)

        source_path = "cookiecutter.json"
        destination_dir = "codejson"
        destination_path = os.path.join(destination_dir, "cookiecutter.json")

        shutil.move(source_path, destination_path)
    
    finally:
        # Moves back to project dir
        os.chdir(original_dir)

def writeLicense():
    """Write a LICENSE that matches the chosen SPDX id (DPG Indicator 2).

    Software MUST use an OSI license; CC0 is invalid for software. The full
    canonical text for common short licenses is written inline; for longer
    licenses we write a clearly-indicated SPDX header + canonical URL and a
    note to paste the full text (so the license is unambiguously indicated).
    """
    holder = ORG_NAME
    spdx = LICENSE_ID
    if not spdx or spdx == "Other":
        return  # leave the existing LICENSE / let the maintainer choose

    if spdx == "MIT":
        text = (
            "MIT License\n\n"
            f"Copyright (c) {holder}\n\n"
            "Permission is hereby granted, free of charge, to any person obtaining a copy "
            "of this software and associated documentation files (the \"Software\"), to deal "
            "in the Software without restriction, including without limitation the rights "
            "to use, copy, modify, merge, publish, distribute, sublicense, and/or sell "
            "copies of the Software, and to permit persons to whom the Software is "
            "furnished to do so, subject to the following conditions:\n\n"
            "The above copyright notice and this permission notice shall be included in all "
            "copies or substantial portions of the Software.\n\n"
            "THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR "
            "IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, "
            "FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE "
            "AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER "
            "LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, "
            "OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE "
            "SOFTWARE.\n"
        )
    else:
        urls = {
            "Apache-2.0": "https://www.apache.org/licenses/LICENSE-2.0.txt",
            "GPL-3.0": "https://www.gnu.org/licenses/gpl-3.0.txt",
            "AGPL-3.0": "https://www.gnu.org/licenses/agpl-3.0.txt",
            "MPL-2.0": "https://www.mozilla.org/media/MPL/2.0/index.txt",
            "BSD-3-Clause": "https://opensource.org/license/bsd-3-clause",
            "CC-BY-4.0": "https://creativecommons.org/licenses/by/4.0/legalcode.txt",
            "CC-BY-SA-4.0": "https://creativecommons.org/licenses/by-sa/4.0/legalcode.txt",
            "CC0-1.0": "https://creativecommons.org/publicdomain/zero/1.0/legalcode.txt",
            "ODbL-1.0": "https://opendatacommons.org/licenses/odbl/1-0/",
        }
        url = urls.get(spdx, "https://spdx.org/licenses/" + spdx + ".html")
        text = (
            f"SPDX-License-Identifier: {spdx}\n\n"
            f"Copyright (c) {holder}\n\n"
            f"This project is licensed under {spdx}.\n"
            f"Full license text: {url}\n\n"
            f"Paste the complete {spdx} license text below this line before publishing.\n"
        )

    with open("LICENSE", "w") as f:
        f.write(text)


def main():
    writeLicense()
    if ADD_TEAM == "True":
        addTeam()
        
    moveCookiecutterFile()
    
    subprocess.call(["git", "init", "-b", "main"])
    subprocess.call(["git", "add", "."])
    subprocess.call(["git", "commit", "-m", "initial commit"])
    
    if CREATE_REPO == "True":
        createGithubRepo()

    if RECEIVE_UPDATES == "True":
        addTopic()
    
    print(f"\n****************************************")
    print(f"\n✅ {REPO_NAME} has successfully been created!\n")

    
if __name__ == "__main__":
    main()
