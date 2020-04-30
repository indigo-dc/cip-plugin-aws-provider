from setuptools import find_packages
from setuptools import setup


def get_requirements():
    with open('requirements.txt') as fp:
        return fp.read()

setup(
    name='cip_plugin_aws_provider',
    version='1.0',
    description='Amazon Web Services provider for the cloud-info-provider',
    license='Apache License 2.0',

    author='Pablo Orviz',
    author_email='orviz@ifca.unican.es',

    url='http://github.com/indigo-dc/cip-plugin-aws-provider',

    classifiers=['License :: OSI Approved :: Apache Software License',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.4',
                 'Intended Audience :: Information Technology',
                 'Intended Audience :: System Administrators',
                 'Intended Audience :: Developers',
                 'Operating System :: POSIX :: Linux',
                 'Environment :: Console',
                 'Topic :: System :: Monitoring'
                 ],

    packages=find_packages(),
    install_requires=get_requirements(),

    entry_points={
        'cip.providers': [
            'aws = cip_plugin_aws_provider.aws:AwsProvider',
        ],
    },

    zip_safe=False,
)
