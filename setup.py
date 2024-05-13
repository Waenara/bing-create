from setuptools import setup, find_packages
setup(
    name='image_creator',
    version='0.0.1',
    author='Waenara',
    author_email='WaenaraCat@gmail.com',
    description='A simple lightweight AI Image Generator from text description using Bing Image Creator (DALL-E 3)',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Waenara/image-creator',
    packages=find_packages(),
    install_requires=open('requirements.txt').readlines(),
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    keywords='ai dall-e image bing api generator image_creator image-generator ig ic',
    project_urls={
        'Support': 'https://github.com/Waenara/image-creator/issues'
    },
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'image-creator = image_creator.main:main',
        ],
    },
)
