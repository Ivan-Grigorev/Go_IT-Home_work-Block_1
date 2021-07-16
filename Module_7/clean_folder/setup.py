from setuptools import setup, find_namespace_packages


setup(name='clean_folder',
      version=1,
      description='Very useful code',
      url='https://github.com/Ivan-Grigorev',
      author='Ivan Grigorev',
      author_email='iv.st.grigorev@gmail.com',
      license='MIT',
      packages=find_namespace_packages(),
      install_requires=['markdown'],
      entry_points={'console_scripts': ['clean_folder = clean_folder.clean:executing_script']}
      )
