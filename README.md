# CSH Swag

CSH's internal swag store allowing for users to see what products CSH has available, and lets users leave reviews.

Swag also allows for the financial director to manage swag, save receipts and keep track of current venmo balance.

## Development
Swag is built to deploy with Docker on Openshift, however if you want to run locally you can

### Config
Copy `config.env.py` and fill in the necessary details. Reach out to @devinmatte or an RTP for details

Information needed:

- LDAP DN
- LDAP PW
- OIDC Secret
- OIDC Client ID
- Mysql Database

### Dependencies

- [python3](https://www.python.org)
    - pip3
        - pylint
- [nodejs](https://nodejs.org)
    - [npm](https://www.npmjs.com)
        - [gulp](https://gulpjs.com)
    - [yarn](https://yarnpkg.com)
```
pip install -r requirements.txt
npm install -g gulp
yarn install
```

#### If running locally on Fedora...
```
dnf install python-devel openldap-devel
```

#### If running locally on Ubuntu...
```
sudo apt-get install libsasl2-dev python-dev libldap2-dev libssl-dev
```

## Credits

Credit to [ComputerScienceHouse/conditional](https://github.com/ComputerScienceHouse/conditional) the pylint and gulp reference

Credit to [@stevenmirabito](https://github.com/stevenmirabito) for helping me, and putting up with my constant questions
