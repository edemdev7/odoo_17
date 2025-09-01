from odoo import http
from odoo.http import request, Response

class JnpApiController(http.Controller):
    @http.route('/jnp/test', type='json', auth='public', methods=['POST'], csrf=False)
    def test_api(self, **kwargs):
        return {'message': 'API test réussie !'}

    @http.route('/jnp/auth', type='json', auth='public', methods=['POST'], csrf=False)
    def auth_api(self, **kwargs):
        login = kwargs.get('login')
        password = kwargs.get('password')
        if not login or not password:
            return {'error': 'Login et mot de passe requis.'}

        uid = request.session.authenticate(request.db, login, password)
        if uid:
            # Génération d'un token simple (à améliorer en prod)
            import uuid
            token = str(uuid.uuid4())
            # Stocker le token en session ou en base si besoin
            request.session['jnp_token'] = token
            return {'token': token, 'uid': uid}
        else:
            return {'error': 'Identifiants invalides.'}
