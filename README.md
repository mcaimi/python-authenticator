# Simple RESTful TOTP Token Generator

A simple TOTP token generator for popular online services. I made this to learn how to use Flask-Restful to build a simple REST server and because I do *not* trust Google Authenticator on my smartphone.

The service is composed of:

	 1. A RESTful user service that computes and returns tokens in JSON format.
	 2. Client software (python cli, integration script with Rofi)
	 3. An user unit for systemd

Accounts are configured in the "accounts.json" file, and thy are organized in
this format:

    "Google - account1@example.com": {
      "account": "account1.example.com",
      "type": "totp",
      "account_type": "google",
      "shared_secret": "<shared secret here>"
    }

The first line is a string, this can be used to mnemonically identify the service.
In the JSON body, a few parameters are needed:

  - "account": this is the account name (username, email, ecc)
  - "type": The type of the token to be computed. Only TOTP is currently supported.
  - "account_type": this is used to display an icon in the GUI. I have icons for Google, GitHub and Amazon.
  - "shared_secret": The key that is given to the user by the service provider. KEEP IT SAFE.

The service, as of now, can be run only as a user service inside systemd and it does not support multiple user configurations. You can, however, launch multiple instances of the apiserver, one per user.

A PKGBUILD for ArchLinux is also provided.

## CONFIGURATION
1. copy /usr/share/python-authenticator/systemd/python-authenticator.service in your ${HOME}/.config/systemd/user directory
2. Create your accounts json file in ${HOME}/.config/accounts/
3. Enable the user unit with systemctl and start the service.

Optionally you can bind a shortcut (ALT-T for example) to automatically call /usr/local/bin/totp.sh to use the integration with Rofi.

## REQUIREMENTS

  - python version 3.x
  - flask
  - flask restful
  - python-otp-lib (https://github.com/mcaimi/python-otp-lib.git)

If you want to integrate with Rofi, you also need:

 - Rofi (of course)
 - xclip (to copy tokens into the clipboard)

