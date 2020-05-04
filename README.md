# Amazon Web Services (AWS) EC2 plugin for the cloud-info-provider

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

* [Description](#description)
* [Installation](#installation)
* [Configuration](#installation)
* [Important Notice](#important-notice)
* [Contribution](#contribution)
* [License](#license)


## Description
This plugin provides Amazon EC2 support for the `cloud-info-provider` component. It gathers resource data, i.e. images and flavors, from a given Amazon region.

## Installation
Under a `cloud-info-provider` deployment, this plugin can be installed using `pip`:
```
$ pip install git+https://github.com/indigo-dc/cip-plugin-aws-provider
```

## Configuration
No additional configuration is needed. The plugin is added to the `cip.providers` namespace, which is scoped by the cloud-info-provider application.

## Important Notice
This plugin has proven to work with the DEEP-Hybrid-DataCloud fork, in particular with the `cloud-info-provider-deep-0.10.6` release. Thus, it is not yet integrated with the official [cloud-info-provider](https://github.com/EGI-Foundation/cloud-info-provider) version.

## Contribution 
Please check our [contribution](CONTRIBUTING.md) guidelines.

## License
Apache License, Version 2.0
