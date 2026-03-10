from flask import Blueprint,render_template
from core.services.web_services import retrieval_service


main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    docs = retrieval_service.list_docs()
    return render_template('index.html', documents=docs)

