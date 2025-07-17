import requests

class Hudu_API:

    def __init__(self, api_key, base_url):
        self.api_key = api_key
        self.base_url = base_url

    def list_assets(self, company_id:int=0, id:int=0, name:str='', page:int=0, page_size:int=0):
        """
        Get a list of assets
        Query by:
        -company_id
        -id
        -name
        -serial_number
        -page
        -page size
        """
        query = self.return_query(locals())

        return self.fetch_results(self.merge_url(f'{self.base_url}/assets', query))
    
    def list_company_assets(self, company_id, page:int=0, page_size:int=0,archived:bool=False):
        """
        Get a list of assets from a specific commpany

        ## PARAMS ##
        page: the current page of results to retrieve
        archived: set to true to only show archived results
        page_size: the number of results to return per page
        """

        query = self.return_query(locals())

        return self.fetch_results(self.merge_url(f'{self.base_url}/companies/{company_id}/assets', query))
    
    def get_company_asset(self, company_id: int, asset_id: int):
        """
        Return a specific asset from a specific company
        """
        return self.fetch_results(f'{self.base_url}/companies/{company_id}/assets/{asset_id}')
    
    def list_companies(self, page:int=0, page_size:int=0, name:str='', phone_number:str='', website:str='', city:str='', id_number:str='', state:str='', slug:str='', search:str=''):
        """
        Return a list of companies
        """

        query = self.return_query(locals())

        return self.fetch_results(self.merge_url(f'{self.base_url}/companies', query))
    
    def get_specific_company(self, company_id: int):
        """
        Return a specifc company info
        """
        return self.fetch_results(f'{self.base_url}/companies/{company_id}')
    
    def list_folders(self, company_id:str='', in_company:bool=False, page:int=0, page_size:int=0):
        """
        Return a list of folders
        """

        query = self.return_query(locals())

        return self.fetch_results(self.merge_url(f'{self.base_url}/folders', query))
    
    def get_folder(self, folder_id: int):
        """
        Return a specific folder
        """
        return self.fetch_results(f'{self.base_url}/folders/{folder_id}')
    
    def list_groups(self, default:bool=False, search:str='', page:int=0, page_size:int=0):
        """
        Return a list of groups
        """
        query = self.return_query(locals())

        return self.fetch_results(self.merge_url(f'{self.base_url}/groups', query))
    
    def get_group(self, group_id: int):
        """
        Return a specific group
        """
        return self.fetch_results(f'{self.base_url}/groups/{group_id}')
    
    def list_ip_addresses(self, network_id:int=0, address:str='', status:str='', fqdn:str='', asset_id:int=0, company_id:int=''):
        """
        Return a list of ip addresses
        """
        query = self.return_query(locals())
        return self.fetch_results(self.merge_url(f'{self.base_url}/ip_addresses', query))
    
    def get_ip_address(self, ip_id: int):
        """
        Return a specifc ip address by ip id
        """
        return self.fetch_results(f'{self.base_url}/ip_addresses/{ip_id}')
    
    def return_lists(self, query:str='', name:str=''):
        """
        Return a list of lists
        """
        query = self.return_query(locals())
        return self.fetch_results(self.merge_url(f'{self.base_url}/lists', query))
    
    def get_list(self, list_id: int):
        """
        Return a specific list
        """
        return self.fetch_results(f'{self.base_url}/lists/{list_id}')
    
    def list_networks(self, company_id:int=0, slug:str='', name:str='', network_type:int=0, address:str='', location_id:int=0, archived:bool=False):
        """
        Return a list of networks
        """
        query = self.return_query(locals())
        return self.fetch_results(self.merge_url(f'{self.base_url}/networks', query))
    
    def get_network(self, network_id: int):
        """
        Return a specific network by network id
        """
        return self.fetch_results(f'{self.base_url}/networks/{network_id}')
    
    def list_password_folders(self, name:str='', company_id:int=0, search:str='', page:int=0, page_size:int=0):
        """
        Return a list of password folders
        """
        query = self.return_query(locals())
        return self.fetch_results(self.merge_url(f'{self.base_url}/password_folders', query))
    
    def get_password_folder(self, password_folder_id: int):
        """
        Return a specific password folder by folder_id
        """
        return self.fetch_results(f'{self.base_url}/password_folders/{password_folder_id}')
    
    def list_asset_passwords(self, name:str='', company_id:int=0, archived:bool=False,page:int=0,page_size:int=0, slug:str='', search:str=''):
        """
        Return a list of asset passwords
        """
        query = self.return_query(locals())
        return self.fetch_results(self.merge_url(f'{self.base_url}/asset_passwords', query))
    
    def get_asset_password(self, asset_id: int):
        """
        Return a specific asset password
        """
        return self.fetch_results(f"{self.base_url}/asset_passwords/{asset_id}")

    def return_query(self, args):
        query = {}
        for name, value in args.items():
            if name == 'self':
                continue
            if value != '' and value != False and value != 0:
                query[name] = value
        return query

    def merge_url(self, url, payload):
        """
        Merge url with any custom query fields that you may need
        Example: 
        payload = {
            'query_value': 1,
            'query_value2': 2,
            etc
        }

        output: example.com/v1/api/endpoint?query_value=1&query_value2=2
        """

        for idx, value in enumerate(payload):
            if idx == 0:
                url += f'?{value}={payload[value]}'
            else:
                url += f'&{value}={payload[value]}'
        return url

    def fetch_results(self, url, payload='', params='', method='GET'):
        header = {
            "x-api-key": self.api_key
        }

        response=''

        match method:
            case "GET":
                response = requests.get(url, headers=header)
            case "POST":
                response = requests.post(url, headers=header)
            case "PUT":
                response = requests.put(url, headers=header)
            case "DELETE":
                response = requests.delete(url, headers=header)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Hudu API call failed: {response.status_code} {response.text}")