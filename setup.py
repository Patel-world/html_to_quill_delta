from setuptools import setup, find_packages

setup(
    name='html_to_quill_delta',
    version='0.1.0',
    description='Convert HTML content to Quill Delta format',
    author='patel-world',
    author_email='patel.dp2024@gmail.com',
    url='https://github.com/Patel-world/html_to_quill_delta',
    packages=find_packages(),
    install_requires=[
        'beautifulsoup4',
        'quill-delta'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
