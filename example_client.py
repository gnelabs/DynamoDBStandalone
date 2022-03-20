
__author__ = "Nathan Ward"

import boto3


class IntegTests(object):
    def __init__(self):
        #Mock AWS access keys. Can be anything.
        self.aws_access_key_id = 'AKIAIOSFODNN7EXAMPLE'
        self.aws_secret_access_key = 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY'
        
        #Mock region name. Can be anything.
        self.region_name = 'us-east-1'
        
        #Authorization key included in header, linked to nginx configuration in templates/default.conf.template.
        self.example_key = 'examplel1QiLCJhbGciOiJIUzI1Nc3MiOiJPbmxpbmUgSldUIchangeME'
        
        #The endpoint IP (or DNS) of your dynamodb standalone instance.
        self.endpoint_url = 'http://localhost'
    
    def _add_header(self, request, **kwargs):
        """
        Add a custom header to botocore requests to include the auth key.
        """
        request.headers.add_header('x-integ-authorization', 'Bearer {0}'.format(self.example_key))
    
    def authenticated_client(self):
        """
        Returns an authenticated boto3 client where dynamodb requests include the auth header.
        """
        #Boto3 client object, pointing to your endpoint.
        client = boto3.client(
            'dynamodb',
            aws_access_key_id = self.aws_access_key_id,
            aws_secret_access_key = self.aws_secret_access_key,
            region_name = self.region_name,
            endpoint_url = self.endpoint_url
        )
        
        #Register an event before performing sigv4 signing for all DDB requests.\
        #Based off of https://boto3.amazonaws.com/v1/documentation/api/latest/guide/events.html
        event_system = client.meta.events
        event_system.register_first('before-sign.dynamodb.*', self._add_header)
        
        return client
    
    def test_list_tables(self):
        """
        Lists current tables in your dynamodb standalone instance.
        """
        #Test the result. If successful you'll get an HTTP 200.
        client = self.authenticated_client()
        result = client.list_tables()
        
        return result
    
    def test_list_tables_fail(self):
        """
        Fail to list tables, testing the auth mechanism.
        """
        #Regular vanilla client.
        client = boto3.client(
            'dynamodb',
            aws_access_key_id = self.aws_access_key_id,
            aws_secret_access_key = self.aws_secret_access_key,
            region_name = self.region_name,
            endpoint_url = self.endpoint_url
        )
        
        #Test the failure. It should return an HTTP 401.
        result = client.list_tables()
        
        return result
    
    def create_table(self):
        """
        Create a basic table to be used for testing.
        """
        client = self.authenticated_client()
        
        table = client.create_table(
            TableName='Movies',
            KeySchema=[
                {
                    'AttributeName': 'year',
                    'KeyType': 'HASH'  # Partition key
                },
                {
                    'AttributeName': 'title',
                    'KeyType': 'RANGE'  # Sort key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'year',
                    'AttributeType': 'N'
                },
                {
                    'AttributeName': 'title',
                    'AttributeType': 'S'
                },

            ],
            BillingMode='PAY_PER_REQUEST'
        )
        
        return table

