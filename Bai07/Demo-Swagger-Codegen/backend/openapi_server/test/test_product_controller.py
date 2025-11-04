import unittest

from flask import json

from openapi_server.models.product import Product  # noqa: E501
from openapi_server.models.product_input import ProductInput  # noqa: E501
from openapi_server.test import BaseTestCase


class TestProductController(BaseTestCase):
    """ProductController integration test stubs"""

    def test_create_product(self):
        """Test case for create_product

        Tạo sản phẩm mới
        """
        product_input = {"price":32990000,"name":"MacBook Air M3","description":"Laptop siêu nhẹ hiệu năng cao"}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/products',
            method='POST',
            headers=headers,
            data=json.dumps(product_input),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_product(self):
        """Test case for delete_product

        Xóa sản phẩm
        """
        headers = { 
        }
        response = self.client.open(
            '/api/products/{id}'.format(id='id_example'),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_product_by_id(self):
        """Test case for get_product_by_id

        Lấy thông tin sản phẩm theo ID
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/products/{id}'.format(id='id_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_products(self):
        """Test case for get_products

        Lấy danh sách sản phẩm
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/products',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_product(self):
        """Test case for update_product

        Cập nhật sản phẩm
        """
        product_input = {"price":32990000,"name":"MacBook Air M3","description":"Laptop siêu nhẹ hiệu năng cao"}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/products/{id}'.format(id='id_example'),
            method='PUT',
            headers=headers,
            data=json.dumps(product_input),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
