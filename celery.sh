#!/bin/bash


if [[ "${1}" == "celery" ]]; then
  celery --app src.celery_tasks.tasks worker -l INFO
elif [[ "${1}" == "flower"  ]]; then
  celery --app src.celery_tasks.tasks flower
  fi
