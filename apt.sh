#!/bin/sh

sudo apt-get update
sudo apt-get install fzf

mkdir -p "$HOME/.zsh"
git clone https://github.com/sindresorhus/pure.git "$HOME/.zsh/pure"