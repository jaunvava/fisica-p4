# endpoint get post. se for post deve receber form cadastro,e chame um servece fake para proceder
# deve return index.html se for get, cadastro sucess 
# 
# 
from flask import render_template, Blueprint

cadastro_bp = Blueprint

@cadastro_bp.route.__get__("/")
def cadastro():
    return render_template("/cadastro")

    if 