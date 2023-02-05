import uuid

import openai
from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from flask_login import login_required, current_user

openai.api_key = "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"

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route("/get_quote", methods=["POST"])
def get_quote():
    if session.get('token') == None or (request.form.get("token") == session.get('token')):
        personality = request.form.get("personality")
        if personality == '':
            flash('Enter the name of the personality!!', category='error')
            session['token'] = None
            return redirect(url_for('views.home'))
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt="Get a quote by {}".format(personality),
            temperature=0.9,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.6,
            stop=[" Human:", " AI:"]
        )
        # generate a new unique token for the form
        token = str(uuid.uuid4())
        session['token'] = token
        return render_template("home.html", quote=response.choices[0]['text'].strip().split('-')[0],
                            personality=response.choices[0]['text'].strip().split('-')[1], token=token, user=current_user)
    else:
        session['token'] = None
        return redirect(url_for('views.home'))

@views.route("/query", methods=["POST"])
def get_answer():
    if session.get('token') == None or (request.form.get("token") == session.get('token')):
        query = request.form.get("query")
        if query == '':
            flash('Enter your Query!!', category='error')
            session['token'] = None
            return redirect(url_for('views.home'))
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=query,
            temperature=0.9,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.6,
            stop=[" Human:", " AI:"]
        )
        # generate a new unique token for the form
        token = str(uuid.uuid4())
        session['token'] = token
        return render_template("home.html", answer=response.choices[0]['text'], token= token, user=current_user)
    else:
       session['token'] = None
       return redirect(url_for('views.home'))
