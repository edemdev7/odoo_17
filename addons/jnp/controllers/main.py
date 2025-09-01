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
                # Génération d'un token simple avec expiration (24h)
                import uuid, datetime
                token = str(uuid.uuid4())
                expires_at = (datetime.datetime.utcnow() + datetime.timedelta(hours=24)).isoformat()
                request.session['jnp_token'] = token
                request.session['jnp_token_expires'] = expires_at
                return {'token': token, 'uid': uid, 'expires_at': expires_at}
        else:
            return {'error': 'Identifiants invalides.'}

        @http.route('/jnp/secure-test', type='json', auth='public', methods=['POST'], csrf=False)
        def secure_test_api(self, **kwargs):
            token = kwargs.get('token')
            session_token = request.session.get('jnp_token')
            expires_at = request.session.get('jnp_token_expires')
            import datetime
            if not token or not session_token or token != session_token:
                return {'error': 'Token invalide ou manquant.'}
            if not expires_at or datetime.datetime.utcnow() > datetime.datetime.fromisoformat(expires_at):
                return {'error': 'Token expiré.'}
            return {'message': 'Accès sécurisé autorisé !'}
