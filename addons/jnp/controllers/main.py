import json
from odoo import http
from odoo.http import request, Response


# Ajoutez cette route simple dans votre classe JnpApiController
@http.route('/jnp/simple-test', type='http', auth='public', methods=['GET'], csrf=False)
def simple_test(self):
    return "Module JNP chargé avec succès !"