from flask import Blueprint, request, jsonify

wiki_link_bp = Blueprint('wiki_link', __name__)


@wiki_link_bp.route('/api/v1/wiki_link', methods=['POST'])
def get_wiki_link():
    pass
