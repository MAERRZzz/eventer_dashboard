from app import create_app
from flask import render_template

app = create_app()


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def page_not_found(error):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5001')
