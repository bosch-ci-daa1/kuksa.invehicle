import base64
import hashlib
import logging
import json

from requests import Session, Response

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

general_pw = 'mylittlesecret'


class Config:
    def __init__(self, server: str, tenant: str, ):
        self.server = server
        self.tenant = tenant


class HonoClient:
    def __init__(self, config: Config):
        self.logger = logging.getLogger(self.__class__.__module__ + '.' + self.__class__.__name__)
        self.config = config
        self.http = Session()

    def get_device(self, controller_id):
        logger.info('Deviceinfo')
        result = dict()
        response: Response = self.http.get(
            url='{server}/registration/{tenant}/{id}'.format(server=self.config.server, tenant=self.config.tenant, id=controller_id),
        )
        try:
            response.raise_for_status()
            result = response.json()
            print(json.dumps(result, indent=2, sort_keys=True))
        except Exception as e:
            logger.debug(e)
        return result or {}

    def device_authinfo(self, controller_id):
        logger.info('Deviceinfo')
        try:
            response = self.http.get(
                url='{server}/credentials/{tenant}/{id}'.format(server=self.config.server, tenant=self.config.tenant, id=controller_id),
            )
            response.raise_for_status()
            result = response.json()
            print(json.dumps(result, indent=2, sort_keys=True))
        except Exception as e:
            logger.debug(e)
            return {}
        return result or {}

    def register_device(self, controller_id):
        logger.info('Register device')

        response: Response = self.http.post(
            url='{server}/registration/{tenant}'.format(server=self.config.server, tenant=self.config.tenant),
            json={
                'device-id': controller_id,
            }
        )
        try:
            response.raise_for_status()
            self.set_credentials(controller_id)
            return response.status_code
        except Exception as e:
            logger.debug(e)

    def unregister_device(self, controller_id):
        logger.info('Unregister device')

        response = self.http.delete(
            url='{server}/registration/{tenant}'.format(server=self.config.server, tenant=self.config.tenant),
            json={
                'device-id': controller_id,
            }
        )
        try:
            response.raise_for_status()
            result = json.loads(response.content)
            print(json.dumps(result, indent=2, sort_keys=True))

        except Exception as e:
            logger.debug(e)

    @staticmethod
    def encrypt_string(pwd: str):
        hashed_pw = hashlib.sha512(pwd.encode()).digest()
        encoded_pw = base64.standard_b64encode(hashed_pw)
        return encoded_pw

    def set_credentials(self, controller_id):
        logger.info('Set Credentials device')
        try:
            pwd = self.encrypt_string(general_pw)
            response = self.http.post(
                url='{server}/credentials/{tenant}'.format(server=self.config.server, tenant=self.config.tenant),
                # TODO handle password in gui
                json={
                    'device-id': controller_id,
                    'type': 'hashed-password',
                    'auth-id': controller_id,
                    'secrets': [{
                        'hash-function': 'sha-512',
                        'pwd-hash': str(pwd)
                    }],
                }
            )
            response.raise_for_status()
        except Exception as e:
            logger.debug(e)

    # def delete_device(self, controller_id):
    #     logger.info('delete device')
    #     feedback_response = self.http.delete(
    #         url='{server}/rest/v1/targets/{controllerId}'.format(server=self.config.server, controllerId=controller_id),
    #         auth=(self.config.user, self.config.pw),
    #
    #     )
    #     print(feedback_response)


if __name__ == "__main__":
    hono_config = Config('http://13.93.66.252:8080', 'AD_TENANT')
    hono_cli = HonoClient(hono_config)
    # hono_cli.registerDevice('edgy03')
    # hono_cli.setCredentials('edgy03')
    hono_cli.encrypt_string('mylittlesecret')
