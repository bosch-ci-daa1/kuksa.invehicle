import logging
import json
from requests import Session

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ConfigurationError(Exception):
    def __init__(self, *args: object, **kwargs: object) -> None:
        super().__init__(*args, **kwargs)


class Config:
    def __init__(self, server: str, tenant: str, user: str, pw: str):
        self.server = server
        self.tenant = tenant
        self.user = user
        self.pw = pw


class HawkbitClient:
    def __init__(self, config: Config):
        self.logger = logging.getLogger(self.__class__.__module__ + '.' + self.__class__.__name__)
        self.config = config
        self.http = Session()

    def list_devices(self):
        logger.info('Get device info')
        response = self.http.get(
            url='{server}/rest/v1/targets'.format(server=self.config.server),
            auth=(self.config.user, self.config.pw),
        )
        try:
            response.raise_for_status()
            result = json.loads(response.content)
            print(json.dumps(result, indent=2, sort_keys=True))
        except Exception as e:
            logger.debug(e)
            return {}
        return result or {}

    def get_device(self, controller_id):
        logger.info('Get device info')
        result = {}
        response = self.http.get(
            url='{server}/rest/v1/targets/{id}'.format(server=self.config.server, id=controller_id),
            auth=(self.config.user, self.config.pw),
        )

        try:
            if response.status_code == 404:
                return result, 404
            response.raise_for_status()
            result = response.json()
            print(json.dumps(result, indent=2, sort_keys=True))
        except Exception as e:
            logger.debug(e)
        return response.status_code, result

    def create_device(self, controller_id, device_name):
        logger.info('Register device')

        action_href = self.get_device(controller_id)

        if action_href.__len__() == 0:
            response = self.http.post(
                url='{server}/rest/v1/targets'.format(server=self.config.server),
                auth=(self.config.user, self.config.pw),
                json=[dict(
                    controllerId=controller_id,
                    name=device_name)],

            )
            response.raise_for_status()
            result = response.json()
            print(json.dumps(result, indent=2, sort_keys=True))

    def delete_device(self, controller_id):
        logger.info('delete device')
        feedback_response = self.http.delete(
            url='{server}/rest/v1/targets/{controllerId}'.format(server=self.config.server, controllerId=controller_id),
            auth=(self.config.user, self.config.pw),

        )
        print(feedback_response)

    def distributions_info(self):
        logger.info('Get Distributionlist')
        response = self.http.get(
            url='{server}/rest/v1/distributionsets'.format(server=self.config.server),
            auth=(self.config.user, self.config.pw),
        )
        try:
            response.raise_for_status()
            result = response.json()
        except Exception as e:
            logger.debug(e)
            return {}
        return result or {}

    def action_list(self):
        controller_id = str(input("Please enter controllerId:"))
        response = self.http.get(
            url='{server}/rest/v1/targets/{controller_id}/actions'.format(server=self.config.server, controller_id=controller_id),
            auth=(self.config.user, self.config.pw),
        )
        try:
            response.raise_for_status()
            result = response.json()
            print(json.dumps(result, indent=2, sort_keys=True))
        except Exception as e:
            logger.debug(e)
            return {}

    def action_status(self):
        logger.info('retrieving a specific action on a specific target')
        controller_id = str(input("Please enter controllerId:"))
        action_id = str(input("Please enter actionId:"))
        response = self.http.get(
            url='{server}/rest/v1/targets/{controller_id}/actions/{action_id}/status'.format(server=self.config.server, controller_id=controller_id, action_id=action_id),
            auth=(self.config.user, self.config.pw),

        )
        try:
            response.raise_for_status()
            result = response.json()
            print(json.dumps(result, indent=2, sort_keys=True))
        except Exception as e:
            logger.debug(e)
            return {}
