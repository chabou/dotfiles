#/bin/bash

certbot certonly \
--manual \
--key-type rsa \
--email chabou@chabou.fr \
-d "home.chabou.fr" \
--agree-tos \
--preferred-challenges=dns \
--config-dir ~/lets-encrypt \
--work-dir ~/lets-encrypt \
--logs-dir ~/lets-encrypt