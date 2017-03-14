# Maintainer: Marco Caimi <marco.caimi@fastweb.it>
_pkgname=authenticator
pkgname=python-${_pkgname}-git
pkgver=0.1
pkgrel=1
pkgdesc="Simple RESTful TOTP Authenticator for my linux Desktop"
depends=('python')
optdepends=()
license=('GPL')
arch=('any')

_gitremote="http://github.com/mcaimi/python-authenticator.git"
_gitpath="python-${_pkgname}"

build() {
  if [ -d $_gitpath ]; then
    cd $_gitpath && git pull
  else
    git clone $_gitremote $_gitpath
  fi

  msg "GIT pull complete, starting build..."
  cd $srcdir/$_gitpath
  python setup.py build
}

package() {
  msg "starting package().."
  # install libraries
  cd $srcdir/$_gitpath
  python setup.py install --root="$pkgdir" --optimize=1

  # install configuration files
  install -D -m0644 "$srcdir/$_gitpath/apiserver.py" "$pkgdir/usr/local/bin/apiserver.py"
  install -D -m0644 "$srcdir/$_gitpath/accounts.json.example" "$pkgdir/usr/share/python-authenticator/accounts/accounts.json.example"
  install -D -m0644 "$srcdir/$_gitpath/config/api-routing.json" "$pkgdir/etc/python-authenticator/api-routing.json"
  install -D -m0644 "$srcdir/$_gitpath/config/api-methods.json" "$pkgdir/etc/python-authenticator/api-methods.json"
  install -D -m0644 "$srcdir/$_gitpath/config/parameters.json" "$pkgdir/etc/python-authenticator/parameters.json"
  install -D -m0644 "$srcdir/$_gitpath/python-authenticator.service" "$pkgdir/usr/share/python-authenticator/systemd/python-authenticator.service"
  install -D -m0644 "$srcdir/$_gitpath/assets/icons/default.png" "$pkgdir/usr/share/python-authenticator/assets/icons/default.png"
  install -D -m0644 "$srcdir/$_gitpath/assets/icons/google.png" "$pkgdir/usr/share/python-authenticator/assets/icons/google.png"
  install -D -m0644 "$srcdir/$_gitpath/assets/icons/github.png" "$pkgdir/usr/share/python-authenticator/assets/icons/github.png"
  install -D -m0644 "$srcdir/$_gitpath/assets/icons/amazon.png" "$pkgdir/usr/share/python-authenticator/assets/icons/amazon.png"

  # install clients
  install -D -m0755 "$srcdir/$_gitpath/pytoken-rofi.py" "$pkgdir/usr/local/bin/pytoken-rofi.py"
  install -D -m0755 "$srcdir/$_gitpath/pytoken-gui.py" "$pkgdir/usr/local/bin/pytoken-gui.py"
  install -D -m0755 "$srcdir/$_gitpath/totp.sh" "$pkgdir/usr/local/bin/totp.sh"
  install -D -m0755 "$srcdir/$_gitpath/run.sh" "$pkgdir/usr/local/bin/run.sh"
}

