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
    """Test adding an item to a table using the bulk method."""
    table = Table(name='Another Table')
    db.session.add(table)
    db.session.commit()

    response = client.post(f'/table/{table.id}', data={
        'bulk_items': 'Gold Coin:10 ; Silver Coin:5'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"2 item(s) added successfully." in response.data
    assert b"Gold Coin" in response.data
    assert b"(Weight: 10)" in response.data
    assert b"Silver Coin" in response.data
    assert b"(Weight: 5)" in response.data

    item1 = Item.query.filter_by(name='Gold Coin').first()
    assert item1 is not None
    assert item1.weight == 10
    item2 = Item.query.filter_by(name='Silver Coin').first()
    assert item2 is not None
    assert item2.weight == 5

def test_bulk_add_parsing(client, db):
    """Test various parsing scenarios for bulk item adding."""
    table = Table(name='Parsing Test Table')
    db.session.add(table)
    db.session.commit()

    test_string = "  sword; axe; spear:2; knife; rusty dagger:3 ; ; item with : in name : 5 ; bad weight:foo "
    response = client.post(f'/table/{table.id}', data={
        'bulk_items': test_string
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"7 item(s) added successfully." in response.data

    # Check the items in the database
    items = Item.query.filter_by(table_id=table.id).order_by(Item.id).all()
    assert len(items) == 7

    # sword (default weight 1)
    assert items[0].name == 'sword'
    assert items[0].weight == 1

    # axe (default weight 1)
    assert items[1].name == 'axe'
    assert items[1].weight == 1

    # spear (weight 2)
    assert items[2].name == 'spear'
    assert items[2].weight == 2

    # knife (default weight 1)
    assert items[3].name == 'knife'
    assert items[3].weight == 1

    # rusty dagger (weight 3)
    assert items[4].name == 'rusty dagger'
    assert items[4].weight == 3

    # item with : in name (weight 5)
    assert items[5].name == 'item with : in name'
    assert items[5].weight == 5

    # bad weight (default weight 1)
    assert items[6].name == 'bad weight'
    assert items[6].weight == 1

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
