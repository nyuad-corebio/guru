# import os
# from nyuad_cgsb_jira_client.jira_client import jira_client

# for project in jira_client.projects():
#     print(project.key)

#!/usr/bin/env python

"""
Create Easybuild configs from conda packages

Create an EasyBuild Config for a Single Conda Package:

1. You can create an easybuild config using the anaconda client show syntax. If you do not specify a version the latest will be pulled in for you.

    python ./create_eb_configs_from_conda_packages.py module -p bioconda/samtools/1.9 bioconda/trimmomatic/0.39 bioconda/fastqc

Will create the easybuild config files samtools-1.9.eb, trimmomatic-0.39.eb and fastqc-0.11.8.eb

2. Create an EasyConfig Bundle from 1 or more conda packages. This will also create any Conda EasyConfigs

    python ./create_eb_configs_from_conda_packages.py bundle -n qc -v 1.0 -p bioconda/trimmomatic/0.39 bioconda/fastqc

3. Create a EasyConfig Bundle from modules (conda or not)

    python ./create_eb_configs_from_conda_packages.py bundle -n qc -v 1.0 -m trimmomatic=0.39 fastqc=0.11.8
"""

from binstar_client.utils import get_server_api, parse_specs
import argparse
from jinja2 import Environment, BaseLoader

aserver_api = get_server_api()


def write_eb_bundle_config(name, version, dependencies):
    eb_bundle_config = '''
easyblock = 'Bundle'

name = '{{name}}'
version = '{{version}}'

#Change the homepage!
homepage = 'none'
description = """Module for {{name}}"""

toolchain = SYSTEM

dependencies = [
    {% for i in dependencies %}
     ('{{i.name}}', '{{i.version}}'),
    {% endfor %}
]

moduleclass = 'tools'
    '''
    data = {
        'name': name,
        'version': version,
        'dependencies': dependencies,
    }
    rtemplate = Environment(loader=BaseLoader).from_string(eb_bundle_config)
    data = rtemplate.render(**data)
    with open("{}-{}.eb".format(name, version), "w") as text_file:
        text_file.write(data)


def write_eb_conda_config(name, version, homepage, summary):
    eb_conda_config = '''##
# This is an easyconfig file for EasyBuild, see https://github.com/easybuilders/easybuild
##

easyblock = 'Conda'

name = "{{name}}"
version = "{{version}}"

homepage = '{{homepage}}'
description = """{{summary}}"""

toolchain = SYSTEM

requirements = "%(name)s=%(version)s"
channels = ['bioconda', 'conda-forge']

builddependencies = [('Miniconda3', '4.7.10')]

sanity_check_paths = {
    'files': ['bin/python'],
    'dirs': ['bin']
}

moduleclass = 'tools'
    '''
    data = {
        'homepage': homepage,
        'name': name,
        'version': version,
        'summary': summary
    }
    rtemplate = Environment(loader=BaseLoader).from_string(eb_conda_config)
    data = rtemplate.render(**data)
    with open("{}-{}.eb".format(name, version), "w") as text_file:
        text_file.write(data)


def get_package_data(package):
    specs = parse_specs(package)
    if not specs._package:
        raise Exception('You did not specify a package!')

    package_data = aserver_api.package(specs.user, specs.package)
    latest_version = package_data['latest_version']
    summary = package_data['summary']
    if specs.user == 'bioconda':
        homepage = 'https://bioconda.github.io/recipes/{}/README.html'.format(specs.package)
    else:
        homepage = 'homepage'

    version = latest_version
    if specs._version:
        version = specs.version

    write_eb_conda_config(specs.package, version, homepage, summary)
    return specs.package, version


def bundle(**kwargs):
    dependencies = []
    for module in kwargs['modules']:
        t = module.split('=')
        dependencies.append({'version': t[1], 'name': t[0]})
    write_eb_bundle_config(kwargs['name'], kwargs['version'], dependencies)


def module(**kwargs):
    for package in kwargs['packages']:
        get_package_data(package)


def conda_bundle(**kwargs):
    dependencies = []
    for package in kwargs['packages']:
        name, version = get_package_data(package)
        dependencies.append({'name': name, 'version': version})
    write_eb_bundle_config(kwargs['name'], kwargs['version'], dependencies)


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title='subcommands',
                                       dest='subparser',
                                       description='valid subcommands',
                                       help='Choose a valid subcommand')
    module_subparser = subparsers.add_parser('module')
    module_subparser.add_argument('--packages', '-p',
                                  nargs='+',
                                  help="""Packages to install as modules.
                                      Package should be in format channel/name or channel/name/version.
                                      Example: bioconda/samtools/1.9
                                      You can specify more than 1 package by putting a space between.
                                      Example: bioconda/samtools/1.9 bioconda/samtools/1.8""")
    bundle_subparser = subparsers.add_parser('bundle')
    bundle_subparser.add_argument('--name', '-n',
                                  required=True,
                                  help="""Module name to use with module load.""")
    bundle_subparser.add_argument('--version', '-v',
                                  required=True,
                                  help="""Module version to use with module load.""")
    bundle_subparser.add_argument('--modules', '-m',
                                  nargs='+',
                                  help="""Modules to include in the bundle.
                                      Package should be in format name=version.
                                      Example: samtools=1.9""")

    conda_bundle_subparser = subparsers.add_parser('conda_bundle')
    conda_bundle_subparser.add_argument('--name', '-n',
                                        required=True,
                                        help="""Module name to use with module load.""")
    conda_bundle_subparser.add_argument('--version', '-v',
                                        required=True,
                                        help="""Module version to use with module load.""")
    conda_bundle_subparser.add_argument('--packages', '-p',
                                        nargs='+',
                                        help="""Packages to install as modules.
                                      Package should be in format channel/name or channel/name/version.
                                      Example: bioconda/samtools/1.9
                                      You can specify more than 1 package by putting a space between.
                                      Example: bioconda/samtools/1.9 bioconda/samtools/1.8""")
    kwargs = vars(parser.parse_args())
    if kwargs['subparser'] is not None:
        subparser = kwargs.pop('subparser')
        globals()[subparser](**kwargs)
    else:
        parser.parse_args(['-h'])


if __name__ == "__main__":
    main()