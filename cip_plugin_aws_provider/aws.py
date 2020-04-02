import copy
import logging

from cloud_info_provider import exceptions
from cloud_info_provider import providers
from cloud_info_provider import utils

try:
    import boto3
except ImportError:
    msg = 'Cannot import boto3.'
    raise exceptions.AwsProviderException(msg)

class AwsProvider(providers.BaseProvider):
    service_type = "compute"
    goc_service_type = None    

    def __init__(self, opts):
        super(AwsProvider, self).__init__(opts)

        if not opts.aws_region_code:
            msg = ('You must provide a AWS Region')
            raise exceptions.AwsProviderException(msg)

        if not opts.aws_access_key or not opts.aws_secret_key:            
            msg = ('You must provide a tuple AWS access key / AWS secret key')
            raise exceptions.AwsProviderException(msg)

        self.aws_region_code = opts.aws_region_code
        self.aws_access_key = opts.aws_access_key
        self.aws_secret_key = opts.aws_secret_key
        
        self.static = providers.static.StaticProvider(opts)

    def setup_logging(self):
        super(AwsProvider, self).setup_logging()
        # Remove info log messages from output
        external_logs = [
            'stevedore.extension',
            'requests',
            'urllib3',
        ]
        log_level = logging.DEBUG if self.opts.debug else logging.WARNING
        for log in external_logs:
            logging.getLogger(log).setLevel(log_level)
   
    def get_images(self, **kwargs):
    #    self.aws_service_name = 'ec2'

        template = {
 #           'image_name': None,
            'image_id': None,
            'image_location': None,
            'image_marketplace_id': None,            
            'image_os_name': None,
            'image_architecture' : None,
            'other_info': [],
        }
        images = {}                
        client = boto3.client('ec2', 
                              region_name=self.aws_region_code, 
                              aws_access_key_id=self.aws_access_key, 
                              aws_secret_access_key=self.aws_secret_key)

        images = client.describe_images(ExecutableUsers=['all'],Filters=[{'Name': 'architecture', 'Values': ['i386']}])
        for i in images['Images']:                               
            print (i['ImageId'])       
            print (i['Architecture'])
            print (i['ImageLocation'])
            print (i['ImageType'])
            aux_img = copy.deepcopy(template)           
            aux_img.update(i)

            # properties
            # property_keys = [_opt for _opt in vars(self.opts)
            #                  if _opt.startswith('property_image_')]
            # d_properties = {}
            # for k in property_keys:
            #     opts_k = vars(self.opts)[k]
            #     v = image.get(opts_k)
            #     d_properties[k] = v
            # aux_img.update(d_properties)
            
            aux_img.update({
                'image_id': i['ImageId'],                                
                'image_architecture': i['Architecture'],
                'other_info': i['ImageLocation']+i['ImageType']
            })            
            images[id] = aux_img
        return images

    @staticmethod
    def populate_parser(parser):
        parser.add_argument(
            '--aws-region',            
            default=utils.env('AWS_DEFAULT_REGION'),
            dest = 'aws_region_code',
            help=('Specify AWS Region Code '
                  '(i. e, us-east-2, ap-south-1, eu-west-3...))'))
        parser.add_argument(
            '--aws-access-key',            
            default=utils.env('AWS_ACCESS_KEY_ID'), 
            dest = 'aws_access_key',
            help=('Specify AWS Access Key ID'))                  

        parser.add_argument(
            '--aws-secret-key',            
            default=utils.env('AWS_SECRET_ACCESS_KEY'), 
            dest = 'aws_secret_key',
            help=('Specify AWS Secret Access Key for'
                  ' the provided AWS Access Key ID'))
