# coding: utf8
from pprint import pprint

from flask import Blueprint, render_template, flash, request
from flask import current_app as app

from .. import __version__
from ..vars import INFO

bp = Blueprint('overview', __name__, url_prefix='/')
check_latest_version = True


@bp.route('/<int:node>/overview/<opt>/<project>/<version_job>/<spider>/', methods=('GET', 'POST'))
@bp.route('/<int:node>/overview/<opt>/<project>/<version_job>/', methods=('GET', 'POST'))
@bp.route('/<int:node>/overview/<opt>/<project>/', methods=('GET', 'POST'))
@bp.route('/<int:node>/overview/', methods=('GET', 'POST'))
def overview(node, opt=None, project=None, version_job=None, spider=None):
    global check_latest_version
    check_latest_version_ = check_latest_version
    if check_latest_version:
        check_latest_version = False

    SCRAPYD_SERVERS = app.config.get('SCRAPYD_SERVERS', ['127.0.0.1:6800'])

    if len(SCRAPYD_SERVERS) == 1:
        flash("Run ScrapydWeb with argument '-ss 127.0.0.1 -ss 192.168.0.101:12345@group1' \
              to set any number of Scrapyd servers to control.", INFO)

    if request.method == 'POST':
        pprint(request.form)
        selected_nodes = []
        for i in range(1, len(SCRAPYD_SERVERS) + 1):
            if request.form.get(str(i)) == 'on':
                selected_nodes.append(i)
    else:
        if len(SCRAPYD_SERVERS) == 1:
            selected_nodes = [1]
        else:
            selected_nodes = []

    return render_template('scrapydweb/overview.html', node=node,
                           scrapydweb_version=__version__,
                           check_latest_version=check_latest_version_,
                           opt=opt, project=project, version_job=version_job, spider=spider,
                           selected_nodes=selected_nodes)
