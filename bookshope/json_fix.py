import json

with open("fixtures/product_fixtures.json", "r") as f:
    data = json.load(f)

for i, item in enumerate(data, start=1):
    if "fields" in item and "product_image" in item["fields"]:
        item["fields"]["product_image"] = f"ecommerce/product_images/ ({i}).jpg"

with open("fixtures/product_fixtures.json", "w") as f:
    json.dump(data, f, indent=2)