#!/bin/bash

CMDDIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
SERVICES=("ec2" "s3")




for service in "${SERVICES[@]}"
do
  scrape $service
done
