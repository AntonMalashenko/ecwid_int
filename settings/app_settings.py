import os

API_PUBLIC_TOKEN = 'public_7iafLdaH32FtCLZkNpyWZtanChFckvbK'
API_PRIVATE_TOKEN = 'secret_nHy9gyXH85QfDmHQHJHRcA79j7YWpKp9'
STORE_ID = '17138055'

BASE_ECWID_URL = 'https://app.ecwid.com'

ORDER_DETAIL_URL_TEMPLATE = '/api/v3/{store_id}/orders/{order_id}'

ORDER_SEARCH_URL_TEMPLATE = '/api/v3/{store_id}/orders'
PRODUCT_SEARCH_URL_TEMPLATE = '/api/v3/{}/products?productId={}'

STORE_PROFILE_URL_TEMPLATE = '/api/v3/{store_id}/profile'

TEST_ORDERS = [66, 67 ,68]

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), ".."),
)

FILES_DIR_NAME = 'generated_files'
FILES_PATH = os.path.join(PROJECT_ROOT, FILES_DIR_NAME)

MAX_PRODUCT_LENGTH = 100


API_PUBLIC_TOKEN = 'public_aFqbCPNH6byGzTgrayjMsM2GttF5k6sH'
API_PRIVATE_TOKEN = 'secret_ceKiyH8E32x98tiiY72D3FhtfiKZsY93'
STORE_ID = '15554429'
