"""Model - Image

"""

from flask import Blueprint

ctrl_image = Blueprint('image', __name__, url_prefix='/image')

@ctrl_image.route('')
def index():
	return str(
		{
		"hello"
		}
	)

# End File: pignus/src/pignus_api/api/modles/ctrl_image.py
