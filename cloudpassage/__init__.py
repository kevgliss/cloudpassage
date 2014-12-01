#simple cloudpassage connector
import sys
import requests
from json import dumps
from urllib import quote

class CloudPassage(object):
    def __init__(self, base_url, key_id, secret_key, verbose=False):
        self.base_url = base_url
        self.verbose = verbose
        self.key_id = key_id
        self.secret_key = secret_key
        self.session = requests.session()
        self.auth_header = self.auth()

    def _args(self, kwargs):
        return '?' + '&'.join("%s=%s" % (quote(key), quote(val))
                                                for key, val
                                                in kwargs.iteritems())

    def _join(self, *parts):
        if not parts:
            return self.base_url

        #if not self.base_url.endswith("/"):
        #    self.base_url += "/"

        url = self.base_url

        for part in parts:
            if part.startswith('/') and url.endswith('/'):
                part = part[1:]

            if not part.startswith("/"):
                url += "/"

            url += part

        return url

    def auth(self):
        url = self.base_url + '/oauth/access_token?grant_type=client_credentials'

        if self.verbose:
            print "requesting {}".format(url)

        response = self.session.post(url, verify=False,
                auth=(self.key_id, self.secret_key))

        if response.status_code != 200:
            print "Could not, auth check keys and try again"
            sys.exit(1)

        elif response.status_code == 200:
            token = response.json()['access_token']
            return {"Authorization":"Bearer {}".format(token)}

    def post(self, method, files=None, data=None, **kwargs):
        url = self._join(method) + self._args(kwargs)

        if self.verbose:
            print "requesting %s" % url

        headers = self.auth_header
        headers.update({'Content-Type': 'application/json'})
        response = self.session.post(url, data=dumps(data), verify=False,
                headers=headers)

        return response

    def get(self, method, **kwargs):
        url = self._join(method) + self._args(kwargs)

        if self.verbose:
            print "requesting %s" % url

        headers = self.auth_header
        headers.update({
                    'Accept': 'application/json'
                })

        #try to get a json response up to five times then fail
        #The api fails sometimes
        for i in range(0, 5):
            try:
                response = self.session.get(url, verify=False,
                        headers=headers)

                response.json()
            except ValueError:
                print response.content
                continue
            break

        return response

    def delete(self, method, **kwargs):
        url = self._join(method) + self._args(kwargs)

        if self.verbose:
            print "requesting %s" % url

        headers = self.auth_header
        response = self.session.delete(url, verify=False,
                headers=headers)

        return response

    def put(self, method, data=None, **kwargs):
        url = self._join(method) + self._args(kwargs)

        if self.verbose:
            print "requesting %s" % url

        headers = self.auth_header
        headers.update({'Content-Type': 'application/json'})

        response = self.sessions.put(url, data=dumps(data), verify=False,
                headers=headers)

        return response


class Events(object):
    def __init__(self, cloudpassage):
        self.cp = cloudpassage

    def list(self):
        response = self.cp.get('/v1/events')
        return reponse


class ConfigurationPolicies(object):
    def __init__(self, cloudpassage):
        self.cp = cloudpassage

    def list(self):
        response = self.cp.get('/v1/policies')
        return response


class Servers(object):
    def __init__(self, cloudpassage):
        self.cp = cloudpassage

    def list(self, kwargs):
        response = self.cp.get('/v1/servers', **kwargs)
        return response

    def list_by_group(self, group_id):
        response = self.cp.get('/v1/groups/{}/servers'.format(group_id))
        return response

    def get(self, server_id):
        response = self.cp.get('/v1/servers/{}'.format(server_id))
        return response

    def delete(self, fip_id):
        response = self.cp.delete('/v1/servers/{}'.format(fip_id))
        return response

    def get_all(self):
        servers = []
        for server in self.list({'state':'active'}).json()['servers']:
            servers.append(self.get(server['id']).json()['server'])
        return servers

    def move(self, server_id, group_id):
        data = {'server': {'group_id': group_id}}
        response = self.cp.put('/v1/servers/{}'.format(server_id))
        return response


class ServerGroups(object):
    def __init__(self, cloudpassage):
        self.cp = cloudpassage

    def list(self):
        response = self.cp.get('/v1/groups')
        return response



class FirewallRules(object):
    def __init__(self, cloudpassage):
        self.cp = cloudpassage

    def list(self, firewall_policy_id):
        response = self.cp.get(
                '/v1/firewall_policies/{}/firewall_rules'.format(firewal_policy_id))
        return response

    def get(self, firewall_policy_id, firewall_rule_id):
        response = self.cp.get(
                '/v1/firewall_policies/{}/firewall_rules/{}'.format(firewall_rule_id))
        return response


class FirewallPolicies(object):
    def __init__(self, cloudpassage):
        self.cp = cloudpassage

    def list(self):
        response = self.cp.get('/v1/firewall_policies')
        return response

    def get(self, fip_id):
        response = self.cp.get('/v1/firewall_policies/{}'.format(fip_id))
        return response

    def create(self, data):
        response = self.cp.post('/v1/firewall_policies', data=data)
        return response

    def update(self, fip_id, data):
        response = self.cp.put('/v1/firewall_policies/{}'.format(fip_id), data=data)
        return response

    def delete(self, fip_id):
        response = self.cp.delete('/v1/firewall_policies/{}'.format(fip_id))
        return response

    def get_all(self):
        policies = []
        for policy in self.list().json()['firewall_policies']:
            policies.append(self.get(policy['id']).json()['firewall_policy'])
        return policies



class FileIntegrityPolicies(object):
    def __init__(self, cloudpassage):
        self.cp = cloudpassage

    def list(self):
        response = self.cp.get('/v1/fim_policies')
        return response

    def get(self, fip_id):
        response = self.cp.get('/v1/fim_policies/{}'.format(fip_id))
        return response

    def create(self, data):
        response = self.cp.post('/v1/fim_policies', data=data)
        return response

    def update(self, fip_id, data):
        response = self.cp.put('/v1/fim_policies/{}'.format(fip_id), data=data)
        return response

    def delete(self, fip_id):
        response = self.cp.delete('/v1/fim_policies/{}'.format(fip_id))
        return response

    def get_all(self):
        policies = []
        for policy in self.list().json()['fim_policies']:
            policies.append((policy['id'], self.get(policy['id']).json()['fim_policy']))
        return policies


class FileIntegrityBaselines(FileIntegrityPolicies):
    def list(self, policy_id):
        response = self.cp.get('/v1/fim_policies/{}/baselines'.format(policy_id))
        return response

    def get(self, policy_id, baseline_id):
        response = self.cp.get(
                '/v1/fim_policies/{}/baselines/{}'.format(policy_id, baseline_id))
        return response

    def create(self, policy_id, server_id, comment=None, expires='null'):
        data = {"baseline": {
                    "server_id": server_id,
                    "expires": expires,
                    "comment": comment
                    }
                }

        response = self.cp.post('/v1/fim_policies/{}/baselines'.format(policy_id),
                                    data=data)
        return response

    def delete(self, policy_id, baseline_id):
        response = self.cp.delete('/v1/fim_policies/{}/baselines/{}'.format(policy_id, baseline_id))
        return response

    def get_all(self, policy_id):
        baselines = []
        for baseline in self.list(policy_id).json()['baselines']:
            baselines.append(self.get(policy_id, baseline['id']).json()['baseline'])
        return baselines
