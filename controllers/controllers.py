# -*- coding: utf-8 -*-
import odoo
import logging
import time
from odoo import http
from odoo.http import content_disposition, dispatch_rpc, request, \
    serialize_exception as _serialize_exception, Response
from odoo.exceptions import AccessError, UserError, AccessDenied
from odoo.models import check_method_name
from odoo.service import db, security

_logger = logging.getLogger(__name__)


class CustomBackup(http.Controller):
    @http.route('/web/database/backup-custom', type='http', auth="none", methods=['GET'], csrf=False)
    def backup_custom(self, master_pwd, name, backup_format = 'zip'):
        try:
            odoo.service.db.check_super(master_pwd)
            ts = datetime.datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
            filename = "%s_%s.%s" % (name, ts, backup_format)
            headers = [
                ('Content-Type', 'application/octet-stream; charset=binary'),
                ('Content-Disposition', content_disposition(filename)),
            ]
            dump_stream = odoo.service.db.dump_db(name, None, backup_format)
            response = werkzeug.wrappers.Response(dump_stream, headers=headers, direct_passthrough=True)
            return response
        except Exception as e:
            _logger.exception('Database.backup')
            error = "Database backup error: %s" % (str(e) or repr(e))
            return self._render_template(error=error)


# class CustomBackup(http.Controller):
#     @http.route('/custom_backup/custom_backup/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_backup/custom_backup/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_backup.listing', {
#             'root': '/custom_backup/custom_backup',
#             'objects': http.request.env['custom_backup.custom_backup'].search([]),
#         })

#     @http.route('/custom_backup/custom_backup/objects/<model("custom_backup.custom_backup"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_backup.object', {
#             'object': obj
#         })