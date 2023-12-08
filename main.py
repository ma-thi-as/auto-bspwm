import os, requests, shutil, subprocess
from zipfile import ZipFile

BASES_URL = {
    "fonts" : {
        'cascadia':'https://github.com/ryanoasis/nerd-fonts/releases/download/v3.1.1/CascadiaCode.zip',
        '3270': 'https://github.com/ryanoasis/nerd-fonts/releases/download/v3.1.1/3270.zip'
    },
}
def font_resolver():
    fonts= BASES_URL['fonts'].values()
    if not os.path.exists(f"{os.getcwd()}/Fonts"):
        os.mkdir("Fonts")
    os.chdir("Fonts")
    
    for f in fonts :    
        filename = f[f.rfind("/") + 1:f.rfind("."):]
        extension =f[f.rfind(".")::]
        os.mkdir(filename) if not os.path.exists(f"{os.getcwd()}/{filename}") else print(True)
        os.chdir(filename)
        response = requests.get(f)

        open(f"{filename}{extension}", "wb").write(response.content) 

        with ZipFile(f"{os.getcwd()}/{filename}{extension}", "r") as zObject:
            # Extract all files and directories from the archive
            zObject.extractall()

        # Get a list of all extracted files
        extracted_files = os.listdir()
        # Filter files with not ".tff" extension and delete
        tff_files = [ os.remove(f"{os.getcwd()}/{file}") if not file.endswith('ttf') else file for file in extracted_files ]
        os.chdir("../")
        
    try:
        shutil.move(f"{os.getcwd()}","/usr/local/share/fonts/")
    except FileExistsError as e:
        print("Las fuentes ya existen.",e)
    

def debPackHandler():
    command = "sudo apt install bspwm sxhkd zsh picom"
    packages = subprocess.run(command,shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    print("Output: ", packages.stdout)
    print("Errors Output: ", packages.stderr)
    if packages.returncode == 0:
        print('All ok... [commands executed]: ', packages.args)
    else:
        print('Problems...')


def kittyHandler():
    kitty_path = f'{os.path.expanduser("~")}/.config/kitty'
    if os.path.exists(f"{kitty_path}"):
        shutil.rmtree(kitty_path)
    shutil.copytree("./basics/kitty", f"{kitty_path}")
    return 'Kitty Ok'
        
def bspwmXsxhkdHandler():
    path_dict = { 
        'bspwm' : f'{os.path.expanduser("~")}/.config/bspwm',
    
        'sxhkd' : f'{os.path.expanduser("~")}/.config/sxhkd'
    }
     
    for i in path_dict:
        if os.path.exists(path_dict[i]):
            shutil.rmtree(path_dict[i])    
        shutil.copytree(f'basics/{i}', f'{os.path.expanduser("~")}/.config/{i}')
        subprocess.run(f'chmod +x {path_dict[i]}/{i}rc',shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)

        if os.path.exists(f"{path_dict['bspwm']}/scripts"):
            command = subprocess.run(f"chmod +x {path_dict['bspwm']}/scripts/bspwm_resize",shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    return 'All redy!'
    
kittyHandler()