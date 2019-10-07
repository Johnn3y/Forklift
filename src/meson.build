pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'Forklift')
gnome = import('gnome')

gnome.compile_resources('Forklift',
  'Forklift.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

python3 = import('python3')

conf = configuration_data()
conf.set('PYTHON', python3.find_python().path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'Forklift.in',
  output: 'Forklift',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir')
)

Forklift_sources = [
  '__init__.py',
  'main.py',
  'applicationwindow.py',
  'application.py',
  'cd.py',
  'items.py'
]

install_data(Forklift_sources, install_dir: moduledir)
