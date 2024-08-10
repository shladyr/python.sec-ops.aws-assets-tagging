from setuptools import setup, find_packages

setup(
    name='aws_tagging_tool',
    version='0.1.0',
    description='AWS Tagging Tool for SOC-2 Compliance',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/your-repo/aws-tagging-tool',
    packages=find_packages(),
    install_requires=[
        'boto3>=1.24.0',
        'configparser>=5.3.0',
        'pytest>=7.0.0',
    ],
    classifiers=[
        'Programming Language :: Python :: 3.12',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.12',
)
