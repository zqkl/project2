from flask import render_template,request,redirect,session,flash
from flask_app import app
from flask_app.models.band_model import Bands

@app.route('/add_band')
def add_band():
    return render_template('new_band.html')

@app.route('/adding_band',methods=['POST'])
def adding_band():
    if not Bands.validate_create(request.form):
        return redirect('/add_band')
    data = {
        **request.form,
        'users_id':session['id']
    }
    Bands.create_band(data)
    return redirect('/bands')

@app.route('/delete_band/<int:id>')
def delete_band(id):
    data = {
        'id':id
    }
    Bands.delete_band(data)
    return redirect('/bands')

@app.route('/edit_band/<int:id>')
def edit_band(id):
    one_band = Bands.get_one_band({'id':id})

    return render_template('edit_band.html',one_band= one_band)

@app.route('/editing/<int:id>',methods=['POST'])
def editing(id):
    if not Bands.validate_create(request.form):
        return redirect(f'/edit_band/{id}')
    data={
        **request.form,
        'id':id
    }
    Bands.edit_band(data)
    return redirect('/bands')

@app.route('/my_bands')
def my_bands():
    data={
        'id':session['id']
    }
    one_band = Bands.my_bands(data)
    return render_template('my_bands.html',bands=one_band)