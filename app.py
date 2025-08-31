import os
import random
from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Table, Item, Tag, CustomPage

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rpg_tables.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'a-secret-key-for-flashing' # Necessary for flash messages

db.init_app(app)

@app.cli.command('init-db')
def init_db_command():
    """Creates the database tables."""
    db.create_all()
    print('Initialized the database.')

@app.route('/')
def index():
    tables = Table.query.all()
    custom_pages = CustomPage.query.all()
    return render_template('index.html', tables=tables, custom_pages=custom_pages)

@app.route('/new-table', methods=['GET', 'POST'])
def new_table():
    if request.method == 'POST':
        table_name = request.form['name']
        tag_names = [tag.strip() for tag in request.form['tags'].split(',')]

        new_table = Table(name=table_name)

        for tag_name in tag_names:
            if tag_name:
                tag = Tag.query.filter_by(name=tag_name).first()
                if not tag:
                    tag = Tag(name=tag_name)
                    db.session.add(tag)
                new_table.tags.append(tag)

        db.session.add(new_table)
        db.session.commit()

        return redirect(url_for('table_detail', table_id=new_table.id))

    return render_template('create_table.html')

@app.route('/table/<int:table_id>', methods=['GET', 'POST'])
def table_detail(table_id):
    table = Table.query.get_or_404(table_id)
    if request.method == 'POST':
        bulk_items_str = request.form.get('bulk_items', '')

        if not bulk_items_str.strip():
            flash('No items were entered.', 'warning')
            return redirect(url_for('table_detail', table_id=table.id))

        item_entries = bulk_items_str.split(';')
        items_added_count = 0

        for entry in item_entries:
            entry = entry.strip()
            if not entry:
                continue

            name = entry
            weight = 1

            if ':' in entry:
                parts = entry.rsplit(':', 1)
                name = parts[0].strip()
                try:
                    weight = int(parts[1].strip())
                    if weight < 1:
                        weight = 1
                except (ValueError, IndexError):
                    weight = 1

            if name:
                new_item = Item(name=name, weight=weight, table_id=table.id)
                db.session.add(new_item)
                items_added_count += 1

        if items_added_count > 0:
            db.session.commit()
            flash(f'{items_added_count} item(s) added successfully.', 'success')
        else:
            flash('No valid items were found to add.', 'warning')

        return redirect(url_for('table_detail', table_id=table.id))

    return render_template('table_detail.html', table=table)

@app.route('/table/<int:table_id>/roll')
def roll_table(table_id):
    table = Table.query.get_or_404(table_id)
    if not table.items:
        flash('Cannot roll on an empty table.', 'warning')
        return redirect(url_for('table_detail', table_id=table.id))

    items = table.items
    item_names = [item.name for item in items]
    item_weights = [item.weight for item in items]

    chosen_item_name = random.choices(item_names, weights=item_weights, k=1)[0]

    flash(f'You rolled: {chosen_item_name}', 'success')
    return redirect(url_for('table_detail', table_id=table.id))

@app.route('/new-custom-page', methods=['GET', 'POST'])
def new_custom_page():
    if request.method == 'POST':
        page_name = request.form['name']
        table_ids = request.form.getlist('tables', type=int)

        if not page_name or not table_ids:
            flash('Page name and at least one table are required.', 'warning')
            return redirect(url_for('new_custom_page'))

        new_page = CustomPage(name=page_name)
        tables = Table.query.filter(Table.id.in_(table_ids)).all()
        new_page.tables.extend(tables)

        db.session.add(new_page)
        db.session.commit()

        return redirect(url_for('custom_page', page_uuid=new_page.uuid))

    tables = Table.query.all()
    return render_template('create_custom_page.html', tables=tables)

@app.route('/page/<uuid:page_uuid>')
def custom_page(page_uuid):
    page = CustomPage.query.filter_by(uuid=str(page_uuid)).first_or_404()
    results = []
    for table in page.tables:
        if table.items:
            items = table.items
            item_names = [item.name for item in items]
            item_weights = [item.weight for item in items]
            chosen_item_name = random.choices(item_names, weights=item_weights, k=1)[0]
            results.append({'table_name': table.name, 'result': chosen_item_name})
        else:
            results.append({'table_name': table.name, 'result': 'This table is empty.'})

    return render_template('custom_page.html', page=page, results=results)

if __name__ == '__main__':
    app.run(debug=True)
