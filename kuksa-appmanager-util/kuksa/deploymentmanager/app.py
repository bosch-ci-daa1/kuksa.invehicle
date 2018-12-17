from flask import Flask, render_template, flash, request
from wtforms import Form, validators, StringField

from kuksa.deploymentmanager.services.hawkbit_service import HawkbitClient, Config

DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'SjdnUends821Jsdlkvxh391ksdODnejdDw'

config = Config('http://localhost:8080', 'DEFAULT', 'admin', 'admin')
cli = HawkbitClient(config)


@app.route("/", methods=['GET'])
def get_targets():
    result = cli.targets_info()
    return render_template('index.html', controllers = result)

# TODO URL create-device
# TODO Python code convention


@app.route("/create_target", methods=['GET', 'POST'])
def create_device():
    form = ReusableForm(request.form)
    result = {}
    # print(form.errors)
    if request.method == 'POST':
        id = request.form['device_id']
        name = request.form['device_name']

    if form.validate():
        cli.create_device(id, name)
        result = cli.target_info(controller_id=id)

        flash('New device was created: {} {}'.format(id, name))
    else:
        flash('Error: All Fields are Required')
    return render_template('create_target.html', controller=result, form=form)


@app.route("/get_distribution_list", methods=['GET'])
def get_distributionlist():
    result = cli.distributions_info()
    return render_template('distribution_list.html', distributions=result)


class ReusableForm(Form):
    device_id = StringField('device_id:', validators=[validators.required()])
    device_name = StringField('device_name:', validators=[validators.required()])


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=4000)
