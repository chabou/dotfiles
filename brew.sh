#!/usr/bin/env bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"


# Install command-line tools using Homebrew.

# Ask for the administrator password upfront.
sudo -v

# Keep-alive: update existing `sudo` time stamp until the script has finished.
while true; do sudo -n true; sleep 60; kill -0 "$$" || exit; done 2>/dev/null &

# Make sure we’re using the latest Homebrew.
brew update

# Upgrade any already-installed formulae.
brew upgrade 

# Install GNU core utilities (those that come with OS X are outdated).
# Don’t forget to add `$(brew --prefix coreutils)/libexec/gnubin` to `$PATH`.
brew install coreutils
sudo ln -s /usr/local/bin/gsha256sum /usr/local/bin/sha256sum

# Install some other useful utilities like `sponge`.
brew install moreutils
# Install GNU `find`, `locate`, `updatedb`, and `xargs`, `g`-prefixed.
brew install findutils
# Install GNU `sed`
brew install gnu-sed
# Install Bash 4.
# Note: don’t forget to add `/usr/local/bin/bash` to `/etc/shells` before
# running `chsh`.
brew install bash
brew install bash-completion2

# Install `wget` with IRI support.
brew install wget 

# Install more recent versions of some OS X tools.
brew install vim 

# Install font tools.
brew tap bramstein/webfonttools
brew install sfnt2woff
brew install sfnt2woff-zopfli
brew install woff2

# Install some CTF tools; see https://github.com/ctfs/write-ups.
brew install binutils
brew install nmap

# Install other useful binaries.
brew install ack
brew install dark-mode
#brew install exiv2
brew install git
brew install git-lfs
brew install imagemagick
brew install lua
brew install lynx
brew install p7zip
brew install pigz
brew install pv
brew install rename
brew install rhino
brew install speedtest_cli
brew install ssh-copy-id
brew install testssl
brew install tree
brew install webkit2png
brew install zopfli

brew install z
brew install fzf

brew install nodejs 
brew install yarn
brew install n
brew install deno

brew install ccat
brew install httpie
brew install telnet
brew install tldr


#AWS
brew install awsebcli

#Ambler
brew install pass
brew install gettext && brew link --force gettext


# Cask
brew tap homebrew/cask
brew install --cask google-chrome
brew install --cask firefox
brew install --cask raycast
brew install --cask hyper
brew install --cask visual-studio-code
brew install --cask slack
brew install --cask whatsapp
brew install --cask google-drive
brew install --cask spotify
brew install --cask docker
brew install --cask notion
brew install --cask rectangle
brew install --cask tunnelblick
brew install --cask ngrok
brew install --cask insomnia
brew install --cask audacity
# brew install --cask noor


brew tap homebrew/cask-fonts
brew install --cask font-fira-code

# Remove outdated versions from the cellar.
brew cleanup

# Additional npm installs
yarn global add pure-prompt
