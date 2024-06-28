import os
import requests
from bs4 import BeautifulSoup

linux_dir = "../linux/"

def generate_build_sh(commit_url: str) -> str:
    compile_target = []
    
    response = requests.get(commit_url)
    soup = BeautifulSoup(response.text, "html.parser")
    tables = soup.find_all("table", class_="diffstat")
    for table in tables:
        rows = table.find_all("tr")
        for row in rows:
            upd_td = row.find("td", class_="upd")
            if upd_td:
                diff_file = upd_td.text.strip()
                if ".c" in diff_file:
                    compile_target.append(diff_file.replace(".c", ".o"))
    
    build_sh = "make allyesconfig\n"
    build_sh += "make -j `nproc` "
    build_sh += " ".join(compile_target)
    
    return build_sh
                
def main():
    with open("linux_data.csv", "r") as f:
        lines = f.readlines()
        for line in lines:
            cve_id, backport_url = line.strip().split(",")
            if not backport_url:
                continue
            if not os.path.exists(os.path.join(linux_dir, cve_id, "build.sh")):
                build_sh = generate_build_sh(backport_url)
                if build_sh:
                    with open(os.path.join(linux_dir, cve_id, "build.sh"), "w") as f:
                        f.write(build_sh)
                        print(f"Generate build.sh for {cve_id}")
                    
if __name__ == "__main__":
    main()   