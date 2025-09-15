from odoo import http
from odoo.http import request

class JnpApiController(http.Controller):
    @http.route('/jnp/simple-test', type='json', auth='public', methods=['GET'], csrf=False)
    def simple_test(self):
        return {"message": "Module JNP chargé avec succès !"}
