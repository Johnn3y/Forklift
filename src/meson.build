pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'gtube_dl')
gnome = import('gnome')

gnome.compile_resources('gtube-dl',
  'gtube-dl.gresource.xml',
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
  input: 'gtube-dl.in',
  output: 'gtube-dl',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir')
)

gtube_dl_sources = [
  '__init__.py',
  'main.py',
  'applicationwindow.py',
  'application.py',
  'cd.py',
  'items.py'
]

install_data(gtube_dl_sources, install_dir: moduledir)
