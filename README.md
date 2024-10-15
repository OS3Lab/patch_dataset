# patch_dataset

Patch dataset for backporting.

## Intro

​	Full information on patches in the dataset can be found in [Dataset_config.xlsx](./Dataset_config.xlsx)

​	For each patch case, we use the naming form `<project_name>/<CVE-ID>` to store it in the corresponding folder. For example: [libtiff/CVE-2022-3597](./libtiff\CVE-2022-3597).

​	Under the folder, the structure is roughly as follows:

```shell
$ tree                                 
.
├── build.sh # selectable
├── config.yml
├── test.sh # selectable
├── poc.sh # selectable
├── real.patch # Which contains the ground truth
└── other_files_needed # selectable
```

​	For each patch folder, `comfig.yml` is required. It contains the most critical information about the patch. 

```yaml
project: libtiff
project_url: https://github.com/libsdl-org/libtiff
new_patch: 4746f16253b784287bc8a5003990c1c3b9a03a62
new_patch_parent: 48d6ece8389b01129e7d357f0985c8f938ce3da3
target_release: f789563a3289b79eaf08a0056026e16c1024614e
sanitizer: AddressSanitizer
error_message: "ERROR: AddressSanitizer"
tag: CVE-2022-3597

#                    Version A           Version A(Fixed)     
#   ┌───┐            ┌───┐             ┌───┐                  
#   │   ├───────────►│   ├────────────►│   │                  
#   └─┬─┘            └───┘             └───┘                  
#     │                                                       
#     │                                                       
#     │                                                       
#     │              Version B                                
#     │              ┌───┐                                    
#     └─────────────►│   ├────────────► ??                    
#                    └───┘                   
```

​	In `config.yml`, the following information is included:

* **project:** The project to which this patch belongs.
* **project_url:** Project repository link.
* **new_patch:**  Patch commit id in new version, Version A(Fixed).
* **new_patch_parent:** Patch parent commit, Version A.
* **target_release:** commid id which need to be fixed, Version B.
* **sanitizer:** sanitizer type for PoC, could be empty
* **error_message:** PoC trigger message to make it easier for the agent to catch errors. , could be empty
* **tag**: CVE-ID

​	For `build.sh`, it contains the project's compilation script, which is called by the backport tool for compilation testing. If it does not exist, it will not be compiled and subsequently tested.

​	For `test.sh`, it contains the running scripts for the project testsuite, which is called by the backport tool for testsuite testing. 

​	For `poc.sh`, it contains the running scripts for the CVE's PoC, which is called by the backport tool for PoC testing. 

​	For `other_files_needed`, all the files that may be required for the script can be placed in this folder.
