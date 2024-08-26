# 输入：data.csv
# CVE-2022-3964, ffmpeg, 92f9b28ed84a77138105475beba16c146bdaf984, ad28b01a141703b831256b712e0613281b15fcf0

# 输出：部分填好的 cfg 文件（包括 new_patch_parent, target_release），使用 git format-patch 生成的 real.patch 文件

import os
import re

import requests
from bs4 import BeautifulSoup

proj_url_map = {
    "ffmpeg": "https://github.com/FFmpeg/FFmpeg",
    "glibc": "https://sourceware.org/git/?p=glibc.git",
    "linux": "https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/",
    "qt": "https://github.com/qt/qtbase",
    "electron": "https://github.com/electron/electron",
    "grpc": "https://github.com/grpc/grpc",
    "krb5": "https://github.com/krb5/krb5",
    "argocd": "https://github.com/argoproj/argo-cd",
    "etcd": "https://github.com/etcd-io/etcd",
    "consul": "https://github.com/hashicorp/consul",
}

proj_commit_map = {
    "ffmpeg": "https://github.com/FFmpeg/FFmpeg/commit/",
    "glibc": "https://sourceware.org/git/?p=glibc.git;a=commit;h=",
    "linux": "https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/commit?id=",
    "qt": "https://github.com/qt/qtbase/commit/",
    "electron": "https://github.com/electron/electron/commit/",
    "grpc": "https://github.com/grpc/grpc/commit/",
    "krb5": "https://github.com/krb5/krb5/commit/",
    "argocd": "https://github.com/argoproj/argo-cd/commit/",
    "etcd": "https://github.com/etcd-io/etcd/commit/",
    "consul": "https://github.com/hashicorp/consul/commit/",
}

# proj 与 patch_dataset 文件夹的相对路径
proj_path_map = {
    "ffmpeg": "../../LLM_Backport/source-project/FFmpeg",
    "glibc": "../../LLM_Backport/source-project/glibc",
    "linux": "../../LLM_Backport/source-project/linux-stable",
    "qt": "../../LLM_Backport/source-project/qtbase",
    "electron": "../../LLM_Backport/source-project/electron",
    "grpc": "../../LLM_Backport/source-project/grpc",
    "krb5": "../../LLM_Backport/source-project/krb5",
    "argocd": "argocd/argo-cd",
    "etcd": "etcd/etcd",
    "consul": "consul/consul",
}


def write_patch(proj_name, cve_id, backport_id):
    """
    Write real.patch in {proj_name}/{cve_id}.

    Args:
        proj_name (str): The name of the project.
        cve_id (str): The CVE ID.
        backport (str): The manual backport commit id.

    Returns:
        None
    """
    # 检查 patch_dataset/proj_name/cve 是否存在
    if not os.path.exists(proj_name):
        os.makedirs(proj_name)
    if not os.path.exists(os.path.join(proj_name, cve_id)):
        os.makedirs(os.path.join(proj_name, cve_id))
    if os.path.exists(os.path.join(proj_name, cve_id, "real.patch")):
        os.remove(os.path.join(proj_name, cve_id, "real.patch"))

    # 切换到 project，生成 patch 文件到 patch_dataset/proj_name/cve
    dataset_abs_path = os.getcwd()
    proj_abs_path = os.path.abspath(proj_path_map[proj_name])
    os.chdir(proj_abs_path)
    os.system(
        "git format-patch -1 %s -o %s"
        % (backport_id, os.path.join(dataset_abs_path, proj_name, cve_id))
    )

    # 切换到 patch_dataset/proj_name/cve
    os.chdir(os.path.join(dataset_abs_path, proj_name, cve_id))

    os.system("mv *.patch real.patch")
    print("generate patch file: ", os.path.join(proj_name, cve_id, "real.patch"))

    # 切换回 patch_dataset
    os.chdir(dataset_abs_path)


def write_cfg(
    proj_name, proj_url, cve_id, patch_release, parent_release, parent_backport
):
    """
    Write config.yml in {proj_name}/{cve_id}.

    Args:
        proj_name (str): The name of the project.
        proj_url (str): The url of the project.
        cve_id (str): The CVE ID.
        patch_release (str): The patch release commit id.
        parent_release (str): The parent commit of patch release.
        parent_backport (str): The parent commit of mannual backport.

    Returns:
        None
    """

    # new_patch = patch_release_commit, 主线引入 patch 的 commit
    # new_patch_parent = new_patch 的 parent commit
    # target_release = mannual_backport_commit 的 parent commit
    template = """project: %s
project_url: %s
new_patch: %s
new_patch_parent: %s
target_release: %s
sanitizer: 
error_message: 
tag: %s"""
    template = template % (
        proj_name,
        proj_url,
        patch_release,
        parent_release,
        parent_backport,
        cve_id,
    )

    # 检查 project 文件夹是否存在
    if not os.path.exists(proj_name):
        os.makedirs(proj_name)

    # 检查 cve 文件夹是否存在
    if not os.path.exists(os.path.join(proj_name, cve_id)):
        os.makedirs(os.path.join(proj_name, cve_id))

    # 写入 config 文件
    with open(os.path.join(proj_name, cve_id, "config.yml"), "w") as f:
        f.write(template)
        print("write config file: ", os.path.join(proj_name, cve_id, "config.yml"))


class Project:
    def __init__(self, csv_data: str, commit_url_prefix: str):
        self.commit_id = self.extract_commit_id(csv_data)
        self.commit_url = commit_url_prefix + self.commit_id

    def extract_commit_id(self, csv_data: str) -> str:
        raise NotImplementedError("Subclasses should implement this method")

    def get_parent(self) -> str:
        raise NotImplementedError("Subclasses should implement this method")


class Github(Project):
    def extract_commit_id(self, csv_data: str) -> str:
        if "https:" in csv_data:
            return re.search(r"/commit/([a-z0-9]*)", csv_data).group(1)
        return csv_data

    def get_parent(self) -> str:
        response = requests.get(self.commit_url)
        soup = BeautifulSoup(response.text, "html.parser")
        elements = soup.find_all(class_="sha-block ml-0")
        for element in elements:
            return element.find_all("a")[0]["href"].split("/")[-1]


class Kernel(Project):
    def extract_commit_id(self, csv_data: str) -> str:
        if "https:" in csv_data:
            return re.search(r"\?id=([a-z0-9]*)", csv_data).group(1)
        return csv_data

    def get_parent(self) -> str:
        response = requests.get(self.commit_url)
        soup = BeautifulSoup(response.text, "html.parser")
        parent_th = soup.find("th", string="parent")
        if parent_th:
            parent_tr = parent_th.find_parent("tr")
            if parent_tr:
                link = parent_tr.find("a")["href"]
                return link.split("/")[-1].replace("?id=", "")


def create_project(proj_name: str, csv_data: str, commit_url_prefix: str) -> Project:
    project_classes = {
        "ffmpeg": Github,
        "linux": Kernel,
        "qt": Github,
        "electron": Github,
        "grpc": Github,
        "krb5": Github,
        "argocd": Github,
        "etcd": Github,
        "consul": Github,
    }
    project_class = project_classes.get(proj_name)
    if project_class:
        return project_class(csv_data, commit_url_prefix)
    raise ValueError(f"Unsupported project name: {proj_name}")


# 处理每一行数据
def process_project_line(project_name, release, backport, proj_commit_url):
    handler = create_project(project_name, release, proj_commit_url)
    release_id = handler.commit_id
    parent_release_id = handler.get_parent()

    handler = create_project(project_name, backport, proj_commit_url)
    backport_id = handler.commit_id
    parent_backport_id = handler.get_parent()

    return release_id, parent_release_id, backport_id, parent_backport_id


# 读取csv文件，获取 parent_release 和 parent_backport
def main():
    # CVE-2022-3964, ffmpeg, 92f9b28ed84a77138105475beba16c146bdaf984, ad28b01a141703b831256b712e0613281b15fcf0
    with open("scripts/config_data.csv", "r") as f:
        lines = f.readlines()
        for line in lines:
            cve_id, project_name, release, backport = line.strip().split(",")
            project_url = proj_url_map.get(project_name)
            proj_commit_url = proj_commit_map.get(project_name)

            release_id, parent_release_id, backport_id, parent_backport_id = (
                process_project_line(project_name, release, backport, proj_commit_url)
            )

            write_cfg(
                project_name,
                project_url,
                cve_id,
                release_id,
                parent_release_id,
                parent_backport_id,
            )
            if backport_id:
                write_patch(project_name, cve_id, backport_id)
            else:
                print("backport_id is empty, no real patch")


if __name__ == "__main__":
    if os.path.basename(os.getcwd()) != "scripts":
        print("Please run this script in patch_dataset/scripts folder")
        exit(1)
    else:
        # 切换到 patch_dataset 文件夹
        os.chdir(os.path.dirname(os.getcwd()))
        main()
