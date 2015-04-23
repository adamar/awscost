#!/bin/bash

CMDDIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
SERVICES=("ec2")

scrape(){

  SERVICE=$1

  # Create service directories is they dont exist
  if [ ! -d "${CMDDIR}/${SERVICE}" ]; then
    mkdir "${CMDDIR}/${SERVICE}"
  fi

  # Get all json URLs from the pricing page
  for url in `curl http://aws.amazon.com/${SERVICE}/pricing/ 2>/dev/null | grep 'model:' | sed -e "s/.*'\(.*\)'.*/http:\\1/"`;
  do
      wget --directory-prefix="${CMDDIR}/${SERVICE}" $url
  done

}



for service in "${SERVICES[@]}"
do
  scrape $service
done
