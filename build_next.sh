#!/bin/bash
if [ -z "$NEXT_VERSION" ]
then
	echo "Set the NEXT_VERSION variable"
	exit
fi
podman build -t babylon-homeroom:${NEXT_VERSION} .
podman tag babylon-homeroom:${NEXT_VERSION} quay.io/panni/babylon-homeroom:${NEXT_VERSION}
podman tag babylon-homeroom:${NEXT_VERSION} quay.io/panni/babylon-homeroom:latest
podman push quay.io/panni/babylon-homeroom:${NEXT_VERSION}
podman push quay.io/panni/babylon-homeroom:latest
oc set image deployment babylon-homeroom babylon-homeroom=quay.io/panni/babylon-homeroom:${NEXT_VERSION}
oc get --export deploy babylon-homeroom -o yaml > babylon-homeroom-deployment-export.yaml
