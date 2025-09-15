from odoo import models, fields, api
from datetime import datetime, timedelta, timezone
import uuid

class JnpApiToken(models.Model):
    _name = 'jnp.api.token'
    _description = 'Token API JNP'

    user_id = fields.Many2one('res.users', required=True)
    token = fields.Char(required=True, index=True)
    expires_at = fields.Datetime(required=True)

    @api.model
    def create_token(self, user_id, duration_hours=24):
        token = str(uuid.uuid4())
        expires = datetime.now(timezone.utc) + timedelta(hours=duration_hours)
        # Convertir en naive datetime pour Odoo
        expires = expires.replace(tzinfo=None)
        
        return self.create({
            'user_id': user_id,
            'token': token,
            'expires_at': expires,
        })

    @api.model
    def check_token(self, token):
        now = datetime.now(timezone.utc)
        rec = self.search([('token', '=', token)], limit=1)
        
        if rec and rec.expires_at:
            # Traiter expires_at comme naive et le comparer avec now en naive
            expires_at = rec.expires_at
            now_naive = now.replace(tzinfo=None)
            
            if expires_at > now_naive:
                return rec.user_id.id
        return False