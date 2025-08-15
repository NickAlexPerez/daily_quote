# app/routes.py
import csv
import io
from flask import Blueprint, jsonify, request, render_template, Response
from . import models


bp = Blueprint('quotes', __name__)

@bp.route("/")
def index():
    return render_template("index.html")

@bp.route("/quote")
def get_quote():
    row = models.get_random_quote()
    if row:
        return jsonify({"quote": row['text']})
    return jsonify({"quote": "No quotes available."})

@bp.route("/quote", methods=['POST'])
def add_quote():
    data = request.get_json()
    quote_text = data.get('quote')
    if not quote_text:
        return jsonify({"error": "No quote provided"}), 400

    models.insert_quote(quote_text)
    return jsonify({"message": "Quote added!"}), 201

@bp.route("/quotes")
def get_all_quotes():
    quotes = models.get_all_quotes()
    return jsonify([{"id": q["id"], "text": q["text"]} for q in quotes])

@bp.route("/quote/<int:quote_id>", methods=['PUT'])
def update_quote(quote_id):
    data = request.get_json()
    new_text = data.get('text')
    if not new_text:
        return jsonify({"error": "No quote provided"}), 400

    models.update_quote(quote_id, new_text)
    return jsonify({"message": "Quote updated!"})

@bp.route("/quote/<int:quote_id>", methods=['DELETE'])
def delete_quote(quote_id):
    models.delete_quote(quote_id)
    return jsonify({"message": "Quote deleted!"})

@bp.route('/export/quotes')
def export_quotes():
    quotes = models.get_all_quotes()
    output = io.StringIO()
    output.write('\ufeff')  # Write BOM for UTF-8

    writer = csv.writer(output)
    writer.writerow(['id', 'text'])

    for quote in quotes:
        writer.writerow([quote['id'], quote['text']])

    output.seek(0)

    return Response(
        output,
        mimetype='text/csv; charset=utf-8',
        headers={"Content-Disposition": "attachment; filename=quotes.csv"}
    )
