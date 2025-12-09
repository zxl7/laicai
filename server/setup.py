from setuptools import setup, find_packages
import os

# 读取README.md文件内容
with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='laicai-stock',
    version='0.1.0',
    description='企业级股票数据服务项目',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your@email.com',
    url='https://github.com/yourusername/laicai-stock',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=[
        'fastapi>=0.100.0',
        'uvicorn[standard]>=0.20.0',
        'pydantic>=2.0.0',
        'pydantic-settings>=2.0.0',
        'sqlalchemy>=2.0.0',
        'aiosqlite>=0.19.0',
        'akshare>=1.10.0',
        'python-dotenv>=1.0.0',
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-asyncio>=0.20.0',
            'httpx>=0.25.0',
            'black>=23.0.0',
            'isort>=5.12.0',
            'flake8>=6.0.0',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Topic :: Office/Business :: Financial :: Investment',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Framework :: FastAPI',
    ],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'laicai-stock=main:main',
        ],
    },
)