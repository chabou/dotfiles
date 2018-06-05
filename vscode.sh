#!/bin/sh

ln -s $PWD/vscode/User/settings.json $HOME/Library/Application\ Support/Code/User/settings.json
for i in $(cat vscode/vscode_extensions ); do code --install-extension $i; done