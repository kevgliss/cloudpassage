README
======

This library is intended to be a small wrapper around the Cloudpassage REST API. It will handle tedious tasks such as authentication with the service and communication with various endpoints.

It is important to note that a lot of endpoints and their methods are note yet implemented.

Basic usage:
    
    import cloudpassage
    
    key_id = "XX"
    secret_key = "XX"

    url = 'https://api.cloudpassage.com'
    cp = cloudpassage.CloudPassage(url, key_id, secret_key)
    fip = cloudpassage.FileIntegrityPolicies(cp)
    print fip.list().json()
