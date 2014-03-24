import os, shutil, json
from pprint import pprint 

class ScaffoldDirs:
	
	# Example structure. An array of dicts. required names are type and name. Type is either 'file' or 'dir'.
	# If type is file, there is an optional 'content' key for the content of the file (default is '')
	# If type is dir, there is an optional 'children' key which mirrors the rules of the larger structure
	# TODO structure should be dict, rather than list. name as key makes sense, as 
	_structure = [{ 'name': 'A', 
					'type': 'dir', 
					'children': [ {'name': 'B', 'type': 'dir', 
									'children': [
										{ 'name': 'a.txt', 'type': 'file', 'content': 'test a'},
										{ 'name': 'b.txt', 'type': 'file', 'content': 'test b'}
								]}

					]
				},
				{ 'name': 'c.txt', 'type': 'file' }
	]
	_parent = '.'

	def __init__(self, structure=None, parent=None):
		if parent != None:
			self._parent = parent
		if structure != None:
			if type(structure) is list:
				self._structure = structure
			else:
				with open(structure) as fp:
					self._structure = json.load(fp)
	

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

	@property
	def parent(self):
		"""Get the current voltage."""
		return self._parent

	@parent.setter
	def parent(self, value):
		self._parent = value


	def build(self, opts={}):
		"""Creates directory structure defined by structure under directory parent
		"""		
		defaults = {
			'structure': self.structure,
			'parent': self.parent
		}
		opts = self.extend(defaults, opts)
		pprint(opts)
		for item in opts['structure']:
			name = os.path.join(opts['parent'], item['name'])
			if item['type'] == 'dir':
				if not os.path.exists(name):
					os.mkdir(name)
				if 'children' in item:
					self.build({ 'structure': item['children'], 'parent': name })
			else :
				content = item['content'] if 'content' in item else ''
				with open (name, 'w') as f: f.write (content)
	
	def destroy(self, opts={}):
		"""Deletes directory structure defined by structure under directory parent
		"""				
		defaults = {
			'structure': self.structure,
			'parent': self.parent
		}
		opts = self.extend(defaults, opts)
		for item in opts['structure']:
			name = os.path.join(opts['parent'], item['name'])
			if not os.path.exists(name):
				continue
			if (item['type'] == 'dir'):
				shutil.rmtree(name)
			else:
				os.remove(name)

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
			structure = [{ 'name': instance, 'type': 'dir', 'children': opts['structure'] }]
			self.destroy({'structure': structure, 'parent': opts['parent'] })


	def clone(self, dirname, structure=[]):
		"""Creates structure based on an existing directory and returns it.
		Can be used to set structure or export as json
		"""
		for item in os.listdir(dirname):
			if item in ['.', '..']:
				continue
			name = os.path.join(dirname, item)
			if os.path.isfile(name):
				with open(name, 'r') as f:
					content = f.read()
				structure.append({ 'name': item, 'type': 'file', 'content': content })
			elif os.path.isdir(name):
				structure.append({ 'name': item, 'type': 'dir', 'children': self.clone(name) })
		return structure

	def extend(self, defaults, opts):
		"""Create a new dictionary with a's properties extended by b,
		without overwriting.

		>>> extend({'a':1,'b':2},{'b':3,'c':4})
		{'a': 1, 'c': 4, 'b': 2}
		"""
		return dict(defaults,**opts)



if __name__ == "__main__":
	b = ScaffoldDirs()
	b.destroys()