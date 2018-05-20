#!/bin/bash

count_processes(){
  count=`ps aux | grep python | grep $1 | grep -v grep | wc -l`
  echo $count
}

while getopts ":hn:" OPT
do
  case $OPT in
    h) echo  "Option -n: max number of processes.";;
    n) OPT_FLAG_n=1;OPT_VALUE_n=$OPTARG ;;
    :) echo  "[ERROR] Option argument is undefined.";;   # 
    \?) echo "[ERROR] Undefined options.";;
  esac
done

shift $(($OPTIND - 1))

process_limit=1
if [[ -n "${OPT_FLAG_n+UNDEF}" ]];then
  process_limit=${OPT_VALUE_n}
fi

command=$1
venv=$NNREVERSI_VENV

if [ `count_processes $command` -lt $process_limit ]; then
  cd /opt/NNReversi/django/
  . $venv
  python -u manage.py $command
fi

