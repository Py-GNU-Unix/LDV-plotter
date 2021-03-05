from setuptools import setup

setup(
    name='LDV-plotter',
    version='0.1.0',    
    description='A simple matematical plotter using matplotlib and qt.',
    url='https://github.com/Py-GNU-Unix/LDV-plotter/',
    author='Py-GNU-Unix',
    author_email='py.gnu.unix.moderator@gmail.com',
    license='GPL-3.0',
    packages=['LDV-plotter'],
    install_requires=['PyQt5==5.14',
                      'matplotlib==3.2.2',                     
                      ],

    classifiers=[  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    
    include_package_data=True
)
