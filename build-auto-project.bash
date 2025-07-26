#!/usr/bin/env bash

# color
YELLOW="\033[1;33m"
RESET="\033[0m"
GREEN='\033[0;32m'
RED='\033[0;31m'

# function
# function for show message information
function info_msg {
    echo -e "${YELLOW}$1${NC}"
}

function warning_message {
    echo -e "${RED}$1"
}

# update and upgrade package
function update_upgrade {
    info_msg "Updating and upgrading packages..."
    sudo apt update -y
    sudo apt upgrade -y
}

# packages
package=(apt-transport-https ca-certificates curl software-properties-common net-tools htop btop tree git wget python3 docker docker-composeو python3-certbot-nginx)

# echo -e "${YELLOW}Your server information:${RESET}"
# echo "−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−"
# hostnamectl
# echo "−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−"

PS3="please enter your number, for exit you can enter (q)"
echo $PS3
echo
options=("1)build-new" "2)re-build" "3)exit")

for i in ${options[@]}; do
    echo "$i"
done

read -p "you number is: " name

if [[ ${name} == 1 ]]; then
    echo -e "oops you can choice ${GREEN}${options[0]} ${RESET}lets go"
    echo "−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−"
    echo "we install a series of package, which include this following: "
    for pkg in "${package[@]}"; do
        echo "${pkg}"
    done

    echo "−−−−−−−−−−−−−−−−−−−−−−−−"
    echo "Do you have a special package in mind?"
    read -p "you can add package type here, If you don't know anything, press Enter.: " input_pkg

    if [[ ${input_pkg} ]]; then
        echo "you type this package --> " $input_pkg
        package+=($input_pkg)
        update_upgrade
        sudo apt install ${package[@]} -y
        info_msg "install package succcess"
    # else
    #     update_upgrade
    #     sudo apt install ${package[@]} -y
    fi

    echo
    echo "*******************************************"
    echo "lets cloen project .."
    echo "*******************************************"
    echo

    read -p "enter github for cleon project .. : " github_addr
    git clone $github_addr

    echo
    echo "*******************************************"
    echo

    ls -it .
    cd $(ls -1t | sed -n '1p')
    echo "list dir project is: "
    ls

    echo
    echo "*******************************************************"
    echo

    echo "Because our project is Django, we need to have a .env file"
    read -p "are you create .env file [Y/n] " created
    if [[ ${created} == "Y" ]]; then
        vi .env
    elif [[ ${created} == "n" ]]; then
        warning_message "It is likely that there will be a problem when running or building the project. "
    fi

    echo
    echo "*******************************************************"
    echo

    # change  directory base image
    cd base_image
    echo
    echo "Now we want to build the project."
    sudo docker build . -t vpn69:1.0.0
    info_msg "build base image deon .. "

    echo
    echo "*******************************************************"
    echo

    # certbot
    sudo systemctl stop nginx # stop nginx, because configs certbot
    read -p "enter domain for certbot... " domain_name
    read -p "enter your email for certbot ..." email_certbot
    if [[ ${domain_name} && ${email_certbot} ]]; then
        sudo certbot certonly --standalone -d ${domain_name} --email ${email_certbot} --agree-tos --no-eff-email

    # change directory certbot
    pwd_dir=$(pwd) # cast pwd command into variable pwd_dir
    echo "pwd is: " $pwd_dir
    echo "list dir is" $(ls)
    read -p "enter directory for copy file... " directory
    cd $directory
    echo "pwd is: " $pwd_dir
    echo "list dir is" $(ls)

    echo
    read  -p "enter path dir nginx" path_dir
    cp * $path_dir
    vi Dockerfile
    vi nginx.conf
    echo
    echo "*******************************************************"
    echo

    read -p "enter directory main project contains docker-compose.yml file, if you dont want please enter: " dir
    if [[ ${dir} ]]; then
      cd $dir
    fi

    echo "start build project ... "
    sudo docker-compose up --build
    fi

elif [[ ${name} == 2 ]]; then
    echo "list dir is --> " $(ls)
    read -p "please enter folder project... " folder_name

    if [[ ${folder_name} ]]; then
        cd ${folder_name}
        echo "rebuild project.. "
        bash re-build.bash
    else
        echo "wrong command"
        exit
    fi

elif [[ ${name} == 3 ]]; then
    echo "exiting script"
    exit
fi
