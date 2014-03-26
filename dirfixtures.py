import os, shutil, json
from pprint import pprint 

class DirFixtures:
	count = 0
	# Example structure. An dict of dicts. The only required attributes is type. Type is either 'file' or 'dir'.
	# If type is file, there is an optional 'content' key for the content of the file (default is '')
	# If type is dir, there is an optional 'children' key which mirrors the rules of the larger structure
	# TODO structure should be dict, rather than list. name as key makes sense, as 
	_structure = {
		'A': { 'type': 'dir', 
			'children': { 
				'B': { 'type': 'dir', 
						'children': {
							'a.txt': { 'type': 'file', 'content': 'test a'},
							'b.txt': { 'type': 'file', 'content': 'test b'}
						}
					}
			}
		},
		'c.txt': { 'type': 'file' }
	}
	_parent = '.'

	_instances = ['local', 'remote']

	def __init__(self, structure=None, parent=None, instances=None):
		# structure
		if structure != None:
			if type(structure) is list:
				self._structure = structure
			else:
				with open(structure) as fp:
					self._structure = json.load(fp)
		# parent
		if parent != None:
			self._parent = parent
		#instances
		if instances != None:
			self._instances = instances
	
	#### Properties
	# structure
	@property
	def structure(self):
		"""Get the current structure."""
		return self._structure

	@structure.setter
	def structure(self, value):
		if type(value) is list:
			self._structure = value
		else:
			with open(value) as fp:
				self._structure = json.load(fp)

	# parent
	@property
	def parent(self):
		"""Get the current voltage."""
		return self._parent

	@parent.setter
	def parent(self, value):
		self._parent = value

	# instances
	@property
	def instances(self):
		"""Get the current voltage."""
		return self._instances

	@instances.setter
	def instances(self, value):
		self._instances = value		

	#### Core methods

	def build(self, opts={}):
		"""Creates directory structure defined by structure under directory parent
		"""		
		defaults = {
			'structure': self.structure,
			'parent': self.parent
		}
		opts = self.extend(defaults, opts)
		for name,atts in opts['structure'].items():
			path = os.path.join(opts['parent'], name)
			if atts['type'] == 'dir':
				if not os.path.exists(path):
					os.mkdir(path)
				if 'children' in atts:
					self.build({ 'structure': atts['children'], 'parent': path })
			else :
				content = atts['content'] if 'content' in atts else ''
				with open (path, 'w') as f: f.write (content)
	
	def destroy(self, opts={}):
		"""Deletes directory structure defined by structure under directory parent
		"""				
		defaults = {
			'structure': self.structure,
			'parent': self.parent
		}
		opts = self.extend(defaults, opts)
		for name,atts in opts['structure'].items():
			path = os.path.join(opts['parent'], name)
			if not os.path.exists(path):
				continue
			if (atts['type'] == 'dir'):
				shutil.rmtree(path)
			else:
				os.remove(path)

	def builds(self, opts={}):
		"""Creates multiple directory structures defined by structure each instance under directory parent
		"""
		defaults = {
			'structure': self.structure,
			'parent': self.parent,
			'instances': ['local', 'remote']
		}

		opts = self.extend(defaults, opts)
		for instance in opts['instances']:
			name = os.path.join(opts['parent'], instance)
			if not os.path.exists(name):
				os.mkdir(name)
			self.build({'structure': opts['structure'], 'parent': name})
		
	def destroys(self, opts={}):
		"""Deletes multiple directory structures defined by structure each instance under directory parent
		"""
		defaults = {
			'structure': self.structure,
			'parent': self.parent,
			'instances': ['local', 'remote']
		}
		opts = self.extend(defaults, opts)
		for instance in opts['instances']:
			structure = { instance: {'type': 'dir', 'children': opts['structure'] } }
			self.destroy({'structure': structure, 'parent': opts['parent'] })


	def clone(self, path):
		"""Creates structure based on an existing directory and returns it.
		Can be used to set structure or export as json
		"""
		path = path.replace('~', os.path.expanduser("~"), 1)
		structure = {}
		if os.path.isfile(path):
			return []
		for name in os.listdir(path):
			if name in ['.', '..']:
				continue
			path = os.path.join(path, name)
			if os.path.isfile(path):
				with open(path, 'r') as f:
					content = f.read()
				structure[name] = { 'type': 'file', 'content': content }
			elif os.path.isdir(path):
				children = self.clone(path)
				structure[name] = { 'type': 'dir', 'content': children }
		return structure

	#### helpers

	# trying to bring jQuery.extend to Python
	def extend(self, defaults, opts):
		"""Create a new dictionary with a's properties extended by b,
		without overwriting.

		>>> extend({'a':1,'b':2},{'b':3,'c':4})
		{'a': 1, 'c': 4, 'b': 2}
		http://stackoverflow.com/a/12697215
		"""
		return dict(defaults,**opts)


#### main
if __name__ == "__main__":
	df = DirFixtures()
	# s = b.clone('~/Code/diveintopython-5.4')
	# s = df.clone('local')
	# pprint(s)
	# df.structure = s
	# df.builds()
	# df.destroys()