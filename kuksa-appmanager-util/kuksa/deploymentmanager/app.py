from flask import Flask, render_template, flash, request
from wtforms import Form, validators, StringField

from kuksa.deploymentmanager.services.hawkbit_service import HawkbitClient, Config as hawkbit_service
from kuksa.deploymentmanager.services.hono_service import HonoClient, Config as hono_service

DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'SjdnUends821Jsdlkvxh391ksdODnejdDw'

hawkbit_config = hawkbit_service('http://localhost:8080', 'DEFAULT', 'admin', 'admin')
hawkbit_client = HawkbitClient(hawkbit_config)

hono_config = hono_service('http://13.93.66.252:8080', 'AD_TENANT')
hono_client = HonoClient(hono_config)


@app.route("/", methods=['GET'])
def get_devicelist():
    result = hawkbit_client.list_devices()
    return render_template('index.html', controllers=result)


@app.route("/create_device", methods=['GET', 'POST'])
def create_device():
    form = ReusableForm(request.form)
    result = {}
    if request.method == 'POST':
        id = request.form['device_id']
        name = request.form['device_name']

    if form.validate():
        result, status_code = hawkbit_client.get_device(id)
        if status_code == 404:
            result, status_code = hawkbit_client.create_device(id, name)
            if status_code == 200:
                hono_client.register_device(controller_id=id)
                hono_client.set_credentials(controller_id=id)
                result = hawkbit_client.get_device(controller_id=id)
            flash('New device was created: {} {}'.format(id, name))
        else:
            flash('Error: Device with id {device_id} already exists'.format(device_id=id))
    else:
        flash('Error: All Fields are Required')
    return render_template('create_device.html', controller=result, form=form)


@app.route("/get_device_services", methods=['GET'])
def get_device_services():
    id = request.args.get('device_id')
    result, status_code = hawkbit_client.get_device_distribution(id)
    return render_template('device_services.html', distributions=result)


@app.route("/distribution_set", methods=['GET'])
def get_distribution_set():
    result = hawkbit_client.distribution_set()
    return render_template('distribution_list.html', distributions=result)


class ReusableForm(Form):
    device_id = StringField('device_id:', validators=[validators.required()])
    device_name = StringField('device_name:', validators=[validators.required()])


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=4000)