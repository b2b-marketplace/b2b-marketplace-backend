response_order = [
    {
        "id": 1,
        "user": 1,
        "status": "Created",
        "created_at": "2023-07-24",
        "order_products": [
            {
                "product": {
                    "id": 1,
                    "supplier": {"id": 1, "name": "seller_1"},
                    "sku": "123",
                    "name": "product_1",
                    "image": "http://testserver/media/path/to/image.jpg",
                },
                "quantity": 3,
                "price": "500.00",
                "cost": 1500.0,
            },
        ],
    },
    {
        "id": 2,
        "user": 1,
        "status": "Created",
        "created_at": "2023-07-24",
        "order_products": [
            {
                "product": {
                    "id": 2,
                    "supplier": {"id": 2, "name": "seller_2"},
                    "sku": "123",
                    "name": "product_2",
                    "image": "http://testserver/media/path/to/image.jpg",
                },
                "quantity": 5,
                "price": "500.00",
                "cost": 2500.0,
            },
        ],
    },
]
