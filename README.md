# win-acme-dns-validation-aliyun
A python script for the "dns validation" in the process of getting a SSL certificate from Let's Encrypt.

If you are trying to get a wildcard ssl certificate by [win-acme](https://www.win-acme.com/), using dns validation is the only way to prove your ownership over
the domain. This script is written to automate the process of creating and deleting the
TXT record on the aliyun dns server on acme's demand.

[Documentations on validation with an external script in acme is here.](https://www.win-acme.com/reference/plugins/validation/dns/script)

# Setting up the script
1. Open settings.json using any text editor and replace `YourAccessKeyId` and `YourAccessSecret` with the accessKeyId and accessSecret you get from aliyun.
2. Set the path to the script used for both creating and deleting dns record to this script, and when asked about the arguments, hit enter directly without typing anything, and win-acme will pass the arguments according to its default settings.
## Create record
This script accept argument as acme's default, which is

    create {Identifier} {RecordName} {Token}

## Delete record 
The script also accept argument as acme's default, which is 

    delete {Identifier} {RecordName} {Token}
