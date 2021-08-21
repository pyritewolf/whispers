#!/bin/bash
set -e

# Set up local vars
set -a
source .env

# Set up colors
COLOR_REST="$(tput sgr0)"
COLOR_GREEN="$(tput setaf 2)"
COLOR_MAGENTA="$(tput setaf 5)"
COLOR_LIGHT_BLUE="$(tput setaf 81)"

# set up precommit hooks (this actually needs to happen outside of docker!)
echo "$COLOR_LIGHT_BLUE 🧑‍🔧 Setting up pre-commit... $COLOR_REST"
pip3 install --upgrade pip
pip3 install pre-commit
pre-commit install -f
echo "$COLOR_LIGHT_BLUE ✨ Pre-commit is ready to rumble! $COLOR_REST"

# create database
echo "$COLOR_LIGHT_BLUE 🧑‍🔧 Ensuring DB exists... $COLOR_REST"
docker-compose run --rm api python3 db/init.py $@
echo "$COLOR_LIGHT_BLUE ✨ DB ${POSTGRES_DB} is set up! $COLOR_REST"

# install dependencies
echo "$COLOR_LIGHT_BLUE 🧑‍🔧 Installing frontend dependencies... $COLOR_REST"
docker-compose run --rm ui npm install
echo "$COLOR_LIGHT_BLUE ✨ Frontend dependencies ready! $COLOR_REST"

# Done!
docker-compose stop
echo
echo "$COLOR_GREEN Whispers setup ready! 🎉 $COLOR_REST"
echo "Run$COLOR_MAGENTA docker-compose up$COLOR_REST to get things running"
