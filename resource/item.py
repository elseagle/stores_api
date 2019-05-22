from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3
from models.item import ItemModel


class Item(Resource):
    # TABLE_NAME = 'items'

    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    parser.add_argument('store_id',
        type=float,
        required=True,
        help="Every item needs a store_id"
    )
    @jwt_required()
    def get(self, name):
        return {"item": [item.json() for itwm in ItemModel.query.all()]}

  

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}

        data = Item.parser.parse_args()
        
        print(name, data['price'], data['store_id'])
        # item = {'name': name, 'price': data['price']}

        try:
            item = ItemModel(name, data['price'], data['store_id'])
            item.save_to_db()
            
        except ValueError:
            return {"message": "An error occurred inserting the item."}

        return item.json()

    

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {"message": "item deleted successfully"}
        return {"message": "item not found "}

        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()

        # query = "DELETE FROM {table} WHERE name=?".format(table=self.TABLE_NAME)
        # cursor.execute(query, (name,))

        # connection.commit()
        # connection.close()

        return {'message': 'Item deleted'}

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItmeModel.find_by_name(name)
        
        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
            # item.price = data['store_id']
        
        item.save_to_db()
        return item.json()
    
 

class ItemList(Resource):
    TABLE_NAME = 'items'

    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM {table}".format(table=self.TABLE_NAME)
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({'name': row[0], 'price': row[1]})
        connection.close()

        return {'items': items}
