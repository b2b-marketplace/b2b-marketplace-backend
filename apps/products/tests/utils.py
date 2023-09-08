PRODUCT_RESPONSE = {
    "id": 11,
    "seller": {"id": 2, "name": "OOO Название"},
    "category": {"id": 1, "name": "Категория-1", "slug": "kategoriya-1", "parent_id": 3},
    "sku": "789",
    "name": "789",
    "brand": "789",
    "price": "789.00",
    "wholesale_quantity": 789,
    "videos": [{"video": "http://host.ru/media/products/kategoriya-1/789/video.mp4"}],
    "quantity_in_stock": 789,
    "description": "789",
    "manufacturer_country": "789",
    "images": [{"image": "http://host.ru/media/products/kategoriya-1/789/image.bmp"}],
    "is_favorited": "false",
}

PRODUCT_CREATE_REQUEST = {
    "sku": "789",
    "name": "789",
    "brand": "Some brand",
    "price": "789.00",
    "wholesale_quantity": 789,
    "quantity_in_stock": 789,
    "description": "Some description",
    "manufacturer_country": "China",
    # TODO
}
