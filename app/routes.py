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

@bp.route('/tags')
def get_all_tags():
    tags = models.get_all_tags()
    return jsonify([{"id": t["id"], "name": t["name"]} for t in tags])

@bp.route('/tag', methods=['POST'])
def add_tag():
    data = request.get_json()
    tag_name = data.get('name')
    if not tag_name:
        return jsonify({"error": "No tag name provided"}), 400

    models.insert_tag(tag_name)
    return jsonify({"message": "Tag added!"}), 201

@bp.route('/tag/<int:tag_id>', methods=['PUT'])
def update_tag(tag_id):
    data = request.get_json()
    new_name = data.get('name')
    if not new_name:
        return jsonify({"error": "No tag name provided"}), 400

    models.update_tag(tag_id, new_name)
    return jsonify({"message": "Tag updated!"})

@bp.route('/tag/<int:tag_id>', methods=['DELETE'])
def delete_tag(tag_id):
    models.delete_tag(tag_id)
    return jsonify({"message": "Tag deleted!"})

@bp.route('/quote/<int:quote_id>/tags')
def get_quote_tags(quote_id):
    tags = models.get_quote_tags(quote_id)
    return jsonify([{"id": t["id"], "name": t["name"]} for t in tags])

@bp.route('/quote/<int:quote_id>/tag', methods=['POST'])
def add_tag_to_quote(quote_id):
    data = request.get_json()
    tag_id = data.get('tag_id')
    if not tag_id:
        return jsonify({"error": "No tag ID provided"}), 400

    models.add_tag_to_quote(quote_id, tag_id)
    return jsonify({"message": "Tag added to quote!"}), 201

@bp.route('/quote/<int:quote_id>/tag/<int:tag_id>', methods=['DELETE'])
def remove_tag_from_quote(quote_id, tag_id):
    models.remove_tag_from_quote(quote_id, tag_id)
    return jsonify({"message": "Tag removed from quote!"})

@bp.route('/quote/<int:quote_id>/available-tags')
def get_available_tags(quote_id):
    tags = models.get_available_tags_for_quote(quote_id)
    return jsonify([{"id": t["id"], "name": t["name"]} for t in tags])
