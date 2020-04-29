import copy
import json
import logging
import re

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

    def _normalize_image_values(self, d_images):
        normalized_values = {
            # image_os_type
            'Linux/UNIX': 'linux',
            'Windows': 'windows',
            # image_architecture
            'i386': 'i686'
        }
        d = {}
        for k, v in d_images.items():
            value = None
            try:
                value = normalized_values[v]
            except Exception:
                value = v
            d[k] = value
        return d

    def _get_distro_version(self, image_name, distro):
        os_regexp = {
            'centos': 'CentOS Linux ([0-9]+) .+'
        }
        try:
            version = re.search(os_regexp[distro], image_name).groups()[0]
        except IndexError:
            version = None
        return version

    def get_images(self, **kwargs):
        images = {}

        template = {
            'image_name': None,
            'image_id': None,
            'image_os_name': None,
            'image_architecture' : None,
            'image_marketplace_id' : None,
        }
        defaults = self.static.get_image_defaults(prefix=True)
        client = boto3.client('ec2',
                              region_name=self.aws_region_code,
                              aws_access_key_id=self.aws_access_key,
                              aws_secret_access_key=self.aws_secret_key)

        # FIXME(orviz) Use filters from file
        _filters = {
            #"ubuntu":[
            #    {"Name": "architecture", "Values": ["x86_64"]},
            #    {"Name": "state", "Values": ["available"]},
            #    {"Name": "root-device-type", "Values": ["ebs"]},
            #    {"Name": "is-public", "Values": ["true"]},
            #    {"Name": "name", "Values": ["ubuntu/images/*%s*"]},
            #    #{'Name': 'name', 'Values': ['ubuntu/images/*2020*']},
            #    {"Name": "owner-id", "Values": ["099720109477"]}
            #],
            "centos": [
                {"Name": "architecture", "Values": ["x86_64"]},
                {"Name": "state", "Values": ["available"]},
                {"Name": "root-device-type", "Values": ["ebs"]},
                {"Name": "is-public", "Values": ["true"]},
                {"Name": "product-code", "Values": ["aw0evgkw8e5c1q413zgy5pjce"]},
                {"Name": "owner-id", "Values": ["679593333241"]}
            ]
		}

        for _distro, _filter in _filters.items():
            image_data = client.describe_images(ExecutableUsers=['all'],Filters=_filter)
            for image in image_data['Images']:
                img_id = image.get('ImageId')

                aux_img = copy.deepcopy(template)
                aux_img.update(defaults)
                aux_img.update(image)

                _image_os_version = self._get_distro_version(image.get('Name'), _distro)
                aux_img.update({
                    'image_id': image.get('ImageId'),
                    'image_name': image.get('Name'),
                    'image_architecture': image.get('Architecture'),
                    'image_os_type': image.get('PlatformDetails'),
                    'image_os_name': _distro,
                    'image_os_version': _image_os_version,
                    'image_marketplace_id': image.get('ImageLocation'),
                })
                images[img_id] = self._normalize_image_values(aux_img)

        return images

    def get_compute_endpoints(self, **kwargs):
        images = self.get_images()
        return {}

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
