PORT="/dev/ttyACM0"
TMP="/tmp/mysense-ttn"
TMPFILE="${TMP}/get_lora_eui.py"
mkdir -p ${TMP}

function get_device_eui() {
  echo -e "from network import LoRa\nimport binascii\nlora = LoRa(mode=LoRa.LORAWAN)\nprint(\"lora_device_eui: \" + binascii.hexlify(lora.mac()).upper().decode('utf-8'))" > ${TMPFILE}
  rshell --quiet -p ${PORT} cp ${TMPFILE} /flash
  echo $(rshell --quiet -p ${PORT} repl \~ import get_lora_eui \~ | grep "lora_device_eui: " | sed 's/^.................//' | sed 's/.$//')
}

function yesno() {
  read -p "${1} (y/n) " result
  if [ ${result} == "y" ]; then
    echo 1
  elif [ ${result} == "n" ]; then
    echo 0
  else
    >&2 echo "Error: please answer with 'y' or 'n'."
    sleep 1
    >&2 echo " "
    return $(yesno "${1}")
  fi
}

function ttnctl() {
  if [ ! -f ${TMP}/ttnctl-linux-amd64 ]; then
    current_dir=$(pwd)
    cd ${TMP}
    wget https://ttnreleases.blob.core.windows.net/release/master/ttnctl-linux-amd64.zip
    unzip ttnctl-linux-amd64.zip
    chmod +x ttnctl-linux-amd64
    echo
    cd ${current_dir}
  fi

  ${TMP}/ttnctl-linux-amd64 ${*}
  if [ "$?" != "0" ]; then
    exit 1
  fi
}

# login to ttn
echo "Please get an access code from: https://account.thethingsnetwork.org/users/authorize?client_id=ttnctl&redirect_uri=/oauth/callback/ttnctl&response_type=code"
read -p "Enter access code: " access_key
echo
ttnctl user login ${access_key}
echo

# create application
read -p "Enter an application id: " app_id
ttnctl applications add ${app_id} ${app_id}
ttnctl applications register
echo

read -p "Enter a name for the devices: " dev_name
echo

count=0
function add_devices() {
  if [ $(yesno "Do you want to add a device?") == "1" ]; then
    echo -e "\nGetting device eui..."
    eui=$(get_device_eui)
    if [ $(echo ${eui} | grep failed | wc -l) != "0" ]; then
      >&2 echo "Error: no device found."
      sleep 1
      >&2 echo " "
      add_devices
      return
    fi
    name="${dev_name}${count}"
    count=$(expr ${count} + 1)
    echo "Found LoPy4 '${name}' with device eui '${eui}'."
    sleep 1

    app_eui=$(ttnctl devices register ${name} ${eui})
    app_key="${app_eui}"

    while [ $(echo ${app_eui} | grep "AppEUI" | wc -l) != "0" ]; do
      app_eui=$(echo ${app_eui} | sed 's/^.//')
    done
    while [ $(echo ${app_eui} | grep " " | wc -l) != "0" ]; do
      app_eui=$(echo ${app_eui} | sed 's/.$//')
    done
    while [ $(echo ${app_eui} | grep "=" | wc -l) != "0" ]; do
      app_eui=$(echo ${app_eui} | sed 's/^.//')
    done

    while [ $(echo ${app_key} | grep "AppKey" | wc -l) != "0" ]; do
      app_key=$(echo ${app_key} | sed 's/^.//')
    done
    while [ $(echo ${app_key} | grep " " | wc -l) != "0" ]; do
      app_key=$(echo ${app_key} | sed 's/.$//')
    done
    while [ $(echo ${app_key} | grep "=" | wc -l) != "0" ]; do
      app_key=$(echo ${app_key} | sed 's/^.//')
    done

    echo -e "antenna_connected = \"true\"\napp_eui = \"${app_eui}\"\napp_key = \"${app_key}\"" > mysense/config/output_lora_otaa.conf
    echo "Flashing MySense..."
    rshell --quiet -p ${PORT} cp -r mysense/* /flash
    echo
    add_devices
  fi
}

add_devices
