pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'Forklift')
gnome = import('gnome')

gnome.compile_resources('Forklift',
  'Forklift.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)

dependency('gtk+-3.0')
dependency('libhandy-0.0')
dependency('libdazzle-1.0')

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
