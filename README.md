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

```
pip install -r requirements.txt
yarn install
gulp
```
