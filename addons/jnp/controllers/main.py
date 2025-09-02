import json
from odoo import http
from odoo.http import request, Response
from functools import wraps


def require_token(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        token = None

        # 1. Vérifier dans le JSON (kwargs)
        if 'token' in kwargs:
            token = kwargs.get('token')

        # 2. Vérifier dans le header Authorization: Bearer xxx
        if not token:
            auth_header = request.httprequest.headers.get("Authorization")
            if auth_header and auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]

        # 3. Vérifier dans les query params ?token=xxx
        if not token:
            token = request.httprequest.args.get("token")

        import json
        if not token:
            return Response(json.dumps({'error': 'Token manquant.'}), content_type='application/json', status=401)

        # Vérifier validité du token
        token_model = request.env['jnp.api.token'].sudo()
        user_id = token_model.check_token(token)
        if not user_id:
            return Response(json.dumps({'error': 'Token invalide ou expiré.'}), content_type='application/json', status=401)

        # Passer l'user_id à la route
        kwargs['user_id'] = user_id
        return func(self, *args, **kwargs)

    return wrapper





class JnpApiController(http.Controller):
    @http.route('/jnp/clients', type='http', auth='public', methods=['GET'], csrf=False)
    @require_token
    def get_clients(self, **kwargs):
        # Pagination
        page = int(request.httprequest.args.get('page', 1))
        limit = int(request.httprequest.args.get('limit', 10))
        offset = (page - 1) * limit

        # Paramètre de filtrage
        filter_type = request.httprequest.args.get('filter', 'client')  # défaut = client

        if filter_type == "all":
            domain = []
        elif filter_type == "proscli":
            domain = [('customer_rank', '>=', 0)]
        else:  # "client"
            domain = [('customer_rank', '>', 0)]

        # Récupération des clients
        clients = request.env['res.partner'].sudo().search(domain, offset=offset, limit=limit)
        total = request.env['res.partner'].sudo().search_count(domain)

        data = [{
            'id': client.id,
            'name': client.name,
            'email': client.email,
            'phone': client.phone,
        } for client in clients]

        response = {
            'clients': data,
            'page': page,
            'limit': limit,
            'total': total,
            'filter': filter_type
        }
        return Response(json.dumps(response), content_type='application/json')


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
            # Génération et stockage du token en base
            token_rec = request.env['jnp.api.token'].sudo().create_token(uid, duration_hours=24)
            return {
                'token': token_rec.token,
                'uid': uid,
                'expires_at': token_rec.expires_at.isoformat()
            }
        else:
            return {'error': 'Identifiants invalides.'}

    @http.route('/jnp/secure-test', type='json', auth='public', methods=['POST'], csrf=False)
    @require_token
    def secure_test_api(self, **kwargs):
        return {'message': 'Accès sécurisé autorisé !'}
