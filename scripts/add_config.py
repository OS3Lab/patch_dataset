# 输入：data.csv
# CVE-2022-3964, ffmpeg, 92f9b28ed84a77138105475beba16c146bdaf984, ad28b01a141703b831256b712e0613281b15fcf0

# 输出：部分填好的 cfg 文件（包括 new_patch_parent, target_release），使用 git format-patch 生成的 real.patch 文件

import os
import requests
from bs4 import BeautifulSoup

proj_url_map = {
    'ffmpeg': 'https://github.com/FFmpeg/FFmpeg'
}

# proj 与 patch_dataset 文件夹的相对路径
proj_path_map = {
    'ffmpeg': '../FFmpeg'
}


def write_patch(proj_name, cve_id, mannual_backport):
    # 检查 project 和 cve 文件夹是否存在
    if not os.path.exists(proj_name):
        os.makedirs(proj_name)
        print('create project folder: ', proj_name)
    if not os.path.exists(os.path.join(proj_name, cve_id)):
        os.makedirs(os.path.join(proj_name, cve_id))
        print('create cve folder: ', os.path.join(proj_name, cve_id))

    # 切换到 project 文件夹，生成 patch 文件
    dataset_abs_path = os.getcwd()
    proj_abs_path = os.path.abspath(proj_path_map[proj_name])
    os.chdir(proj_abs_path)
    os.system('git format-patch -1 %s -o %s' % (mannual_backport,
              os.path.join(dataset_abs_path, proj_name, cve_id)))

    # 切换到cve文件夹
    os.chdir(os.path.join(dataset_abs_path, proj_name, cve_id))
    os.system('mv *.patch real.patch')
    print('generate patch file: ', os.path.join(
        proj_name, cve_id, 'real.patch'))

    # 返回patch_dataset文件夹
    os.chdir(dataset_abs_path)


def write_cfg(proj_name, proj_url, cve_id, patch_release, parent_release, parent_backport):

    # new_patch = patch_release_commit, 主线引入 patch 的 commit
    # new_patch_parent = new_patch 的 parent commit
    # target_release = mannual_backport_commit 的 parent commit
    template = '''project: %s
project_url: %s
new_patch: %s
new_patch_parent: %s
target_release: %s
sanitizer: 
error_massage: 
tag: %s'''
    template = template % (proj_name, proj_url, patch_release,
                           parent_release, parent_backport, cve_id)

    # 检查 project 文件夹是否存在
    if not os.path.exists(proj_name):
        os.makedirs(proj_name)
        print('create project folder: ', proj_name)
    else:
        print('project folder exists: ', proj_name)

    # 检查 cve 文件夹是否存在
    if not os.path.exists(os.path.join(proj_name, cve_id)):
        os.makedirs(os.path.join(proj_name, cve_id))
        print('create cve folder: ', os.path.join(proj_name, cve_id))
    else:
        print('cve folder exists: ', os.path.join(proj_name, cve_id))

    with open(os.path.join(proj_name, cve_id, 'config.yml'), 'w') as f:
        f.write(template)
        print('write config file: ', os.path.join(
            proj_name, cve_id, 'config.yml'))


# 通过 commit url 获取 parent commit
def get_parent_commit(commit_url):
    response = requests.get(commit_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    elements = soup.find_all(class_='sha-block ml-0')
    for element in elements:
        parent_commit = element.find_all('a')[0]['href'].split('/')[-1]
        return parent_commit


# 读取csv文件，获取 parent_release 和 parent_backport
def main():
    # CVE-2022-3964, ffmpeg, 92f9b28ed84a77138105475beba16c146bdaf984, ad28b01a141703b831256b712e0613281b15fcf0
    with open('scripts/data.csv', 'r') as f:
        lines = f.readlines()
        for line in lines:
            cve_id, project, patch_release, mannual_backport = line.strip().split(',')
            project_url = proj_url_map[project]
            if 'https:' in patch_release:
                patch_release = patch_release.split('/')[-1]
            if 'https:' in mannual_backport:
                mannual_backport = mannual_backport.split('/')[-1]

            patch_release_url = project_url + '/commit/' + patch_release
            parent_release = get_parent_commit(patch_release_url)
            mannual_backport_url = project_url + '/commit/' + mannual_backport
            parent_backport = get_parent_commit(mannual_backport_url)

            write_cfg(project, project_url, cve_id, patch_release,
                      parent_release, parent_backport)
            write_patch(project, cve_id, mannual_backport)


if __name__ == '__main__':
    if os.path.basename(os.getcwd()) != 'scripts':
        print('Please run this script in patch_dataset/scripts folder')
        exit(1)
    else:
        # 切换到 patch_dataset 文件夹
        os.chdir(os.path.dirname(os.getcwd()))
        main()
