from models import Table, Item, Tag, CustomPage

def test_index(client):
    """Test that the index page loads."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"RPG Tables" in response.data

def test_create_table(client, db):
    """Test creating a new table."""
    response = client.post('/new-table', data={
        'name': 'Test Table',
        'tags': 'dungeon, monsters'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Test Table" in response.data

    table = Table.query.filter_by(name='Test Table').first()
    assert table is not None
    assert len(table.tags) == 2
    assert table.tags[0].name == 'dungeon'
    assert table.tags[1].name == 'monsters'

def test_add_item_to_table(client, db):
    """Test adding an item to a table."""
    # First, create a table to add items to
    table = Table(name='Another Table')
    db.session.add(table)
    db.session.commit()

    response = client.post(f'/table/{table.id}', data={
        'name': 'Gold Coin',
        'weight': '10'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Gold Coin" in response.data
    assert b"(Weight: 10)" in response.data

    item = Item.query.filter_by(name='Gold Coin').first()
    assert item is not None
    assert item.table_id == table.id
    assert item.weight == 10

def test_roll_table(client, db):
    """Test rolling on a table."""
    table = Table(name='Rolling Table')
    item1 = Item(name='Sword', weight=1, table=table)
    item2 = Item(name='Shield', weight=99, table=table)
    db.session.add_all([table, item1, item2])
    db.session.commit()

    response = client.get(f'/table/{table.id}/roll', follow_redirects=True)
    assert response.status_code == 200
    # The flashed message should contain the result.
    # Since the weight of "Shield" is so high, it's very likely to be the result.
    # In a more robust test, you might mock random.choices. For now, we check for the general message.
    assert b"You rolled:" in response.data
    # Check that one of the items was rolled
    assert (b"Sword" in response.data or b"Shield" in response.data)

def test_roll_empty_table(client, db):
    """Test rolling on an empty table."""
    table = Table(name='Empty Table')
    db.session.add(table)
    db.session.commit()

    response = client.get(f'/table/{table.id}/roll', follow_redirects=True)
    assert response.status_code == 200
    assert b"Cannot roll on an empty table." in response.data

def test_create_custom_page(client, db):
    """Test creating a custom page."""
    table1 = Table(name='Loot Table 1')
    table2 = Table(name='Loot Table 2')
    db.session.add_all([table1, table2])
    db.session.commit()

    response = client.post('/new-custom-page', data={
        'name': 'My Custom Loot Page',
        'tables': [table1.id, table2.id]
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"My Custom Loot Page" in response.data

    page = CustomPage.query.filter_by(name='My Custom Loot Page').first()
    assert page is not None
    assert len(page.tables) == 2

def test_view_custom_page(client, db):
    """Test viewing a custom page and seeing the results."""
    table1 = Table(name='Monster Table')
    item1 = Item(name='Goblin', weight=1, table=table1)
    table2 = Table(name='Treasure Table')
    item2 = Item(name='10 Gold', weight=1, table=table2)

    page = CustomPage(name='Dungeon Roll')
    page.tables.append(table1)
    page.tables.append(table2)

    db.session.add_all([table1, item1, table2, item2, page])
    db.session.commit()

    response = client.get(f'/page/{page.uuid}')
    assert response.status_code == 200
    assert b"Dungeon Roll" in response.data
    assert b"Monster Table:" in response.data
    assert b"Goblin" in response.data
    assert b"Treasure Table:" in response.data
    assert b"10 Gold" in response.data
