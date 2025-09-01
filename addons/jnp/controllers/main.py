from odoo import http
from odoo.http import request, Response

class JnpApiController(http.Controller):
    @http.route('/jnp/test', type='json', auth='public', methods=['POST'], csrf=False)
    def test_api(self, **kwargs):
        return {'message': 'API test réussie !'}
