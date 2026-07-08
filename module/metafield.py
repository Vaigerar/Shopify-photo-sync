import re

import shopify


def add_metafields(sfy_product_id, inventory):
    prod = shopify.Product.find(str(sfy_product_id))
    match = re.search(r'ARTISTS:\s*([^*]+)\*', inventory.description)

    if match:
        artist_name = match.group(1).strip()
        print(artist_name)
    else:
        artist_name = 'Не знайдено'
        print("Ім'я художника не знайдено.")

    prod.add_metafield(
        shopify.Metafield(
            {"namespace": "custom", "key": "materials_2", "value": f"{inventory.Basis}",
             "type": "single_line_text_field"}))
    prod.add_metafield(
        shopify.Metafield(
            {"namespace": "custom", "key": "materials_1", "value": f"{inventory.Materials}",
                           "type": "single_line_text_field"}))
    prod.add_metafield(
        shopify.Metafield(
            {"namespace": "custom", "key": "width", "value": f"{float(inventory.Width)}",
             "type": "number_integer"}))

    prod.add_metafield(
        shopify.Metafield(
            {"namespace": "custom", "key": "artist", "value": f"{artist_name}", "type": "single_line_text_field"}))


    prod.add_metafield(
        shopify.Metafield(
            {"namespace": "custom", "key": "size", "value": f"{float(inventory.Height)}", "type": "number_integer"}))

    prod.add_metafield(
        shopify.Metafield(
            {"namespace": "custom", "key": "subject", "value": f'["{inventory.Subject}"]',
                           "type": "list.single_line_text_field"}))
