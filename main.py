import argparse
import shutil
import json
import os

def replace_test_in_file(file, from_text, to_text):
    print(file, from_text, to_text)
    with open(file) as f:
        newText = f.read().replace(from_text, to_text)     
    with open(file, "w") as f:
        f.write(newText)    

def create_structure(config_file, project_name, option_type):    
    with open(config_file) as file:
        data = json.load(file)   
    dest = '/'    
    if not os.path.isdir('out'):
        os.mkdir('out')
    dest = os.path.dirname(os.path.realpath(__file__))+'/out/'        
    for d in data["folder"]:
        dir_d = dest+d["target"]+d["name"]
        if not os.path.isdir(dir_d):
            os.mkdir(dir_d+"/")    
    for d in data['file']:
        shutil.copy2(d["path"], dest+d["target"])   
    for d in data['file']:
        if d["name"] == "CMakeLists.txt" or d["name"] == "README.md":
            replace_test_in_file(dest+d["target"]+d["name"], "example", project_name)        
        if option_type == 1:
            if d["name"] == "CMakeLists.txt":
                replace_test_in_file(dest+d["target"]+d["name"], "exampleApp", project_name+"App")
                replace_test_in_file(dest+d["target"]+d["name"], "exampleLib", project_name+"Lib")
                replace_test_in_file(dest+d["target"]+d["name"], "exampleTest", project_name+"Test")
            elif d["name"] == "conanfile.py":
                replace_test_in_file(dest+d["target"]+d["name"], "exampleLib", project_name+"Lib")
                replace_test_in_file(dest+d["target"]+d["name"], "exampleConan", project_name+"Conan")

def empty_project_argument(empty_project, project_name):
    option_type = empty_project
    config_file = ""

    if option_type == 0:
        config_file = 'configuration/conan_application.json'
    elif option_type == 1:
        config_file = 'configuration/conan_library.json'

    create_structure(config_file, project_name, option_type)
    print('Done, please check \"out\" folder.')    


def main():
    parser = argparse.ArgumentParser(description='Internal tools')
    parser.add_argument("--project_name", type=str, help="Enter project name")
    parser.add_argument("--empty_project", type=int, choices=[0, 1], 
                        help="Create empty project structure, ({0} - conan CMake app structure), ({1} - conan CMake lib structure)")
    args = parser.parse_args()

    if args.project_name is not None and args.empty_project is not None:
        empty_project_argument(args.empty_project, args.project_name)

if __name__ == "__main__":
    main()