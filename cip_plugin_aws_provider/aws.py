
from cloud_info_provider import providers


class AwsProvider2(providers.BaseProvider):
    def __init__(self, opts):
        super(AwsProvider2, self).__init__(opts)
