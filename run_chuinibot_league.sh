#!/bin/bash

# Activate the Poetry environment
source ~/.cache/pypoetry/virtualenvs/chuinibot-gG20k6B3-py3.10/bin/activate

cd ~/Proyectos/chuinibot

# Run your Python script
python -m chuinibot.entrypoint.main league-send-day
