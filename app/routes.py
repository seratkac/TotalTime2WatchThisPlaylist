# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
import main


server = Flask(__name__)


@server.route('/')
def index():
    return render_template(
        'index.html',
        title="Mianooooooooooooooooooooooooooooooooo"
    )


@server.route('/', methods=['POST'])
def gt():
    playlist_id = request.form['playlist_id']
    spreadsheet_id = request.form['spreadsheet_id']
    smt = main.main(playlist_id, spreadsheet_id)
    try:
        return render_template(
            "index.html",
            total_duration=smt.total_d,
            max_duration=smt.max_duration,
            min_duration=smt.min_duration,
            playlist_id=playlist_id,
            spreadsheet_id=spreadsheet_id
        )
    except Exception as e:
        return e
