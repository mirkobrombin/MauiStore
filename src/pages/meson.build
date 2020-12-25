pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
pagesdir = join_paths(pkgdatadir, 'mauistore/pages')

mauistore_sources = [
  '__init__.py',
  'list.py',
]

install_data(mauistore_sources, install_dir: pagesdir)
