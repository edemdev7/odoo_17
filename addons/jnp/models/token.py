from odoo import models, fields, api
import datetime

class JnpApiToken(models.Model):
    _name = 'jnp.api.token'
    _description = 'Token API JNP'

    user_id = fields.Many2one('res.users', required=True)
    token = fields.Char(required=True, index=True)
    expires_at = fields.Datetime(required=True)


    @api.model
    def create_token(self, user_id, duration_hours=24):
        import uuid
        token = str(uuid.uuid4())
        expires = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=duration_hours)).replace(tzinfo=None)
        return self.create({
            'user_id': user_id,
            'token': token,
            'expires_at': expires,
        })

    @api.model
    def check_token(self, token):
        now = datetime.datetime.now(datetime.timezone.utc)
        rec = self.search([('token', '=', token)])
        if rec and rec.expires_at:
            # Convertir expires_at en timezone-aware si besoin
            expires_at = rec.expires_at
            if expires_at.tzinfo is None:
                expires_at = expires_at.replace(tzinfo=datetime.timezone.utc)
            if expires_at > now:
                return rec.user_id.id
        return False
