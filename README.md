#DirFixtures

The point of this Python module is to easily create, delete, and copy directory structures. It came about because of the larger goal of my [unified-migration-theory](https://github.com/athill/unified-migration-theory) project (whose goal is to migrate files to production servers, based on Git syntax, to servers that don't pull from a repository) which got stonewalled when I discovered the difficulty of maintaining test directories manually. 

One epiphany later, I decided to get back to brass tacks and write a python module that could easily create and destroy directory structures for testing purposes. This is v0.8 of that module.

## Concepts

### Structure
The essence of the functionality is in the *structure* datatype, a dict of dicts representing a directory. For example, a simple structure:

	structure = {
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

Each key has a *type* attribute that is either *file* or *dir*. File types have an optional content attribute with the contents of the file. Dir types have an optional *children* attribute, that mirrors the parent structure. The structure above would generate the following directory tree.

	A/
	  \_B/
	     \_a.txt
	     |
	     |_b.txt
	c.txt

Structures can be generated from an existing directory via the clone() method or loaded from a JSON file

### Parent
Parent is where to build the directory structure(s). The default is the current directory ('.'). It's a string and expects a *nix path (e.g., '/var/www/html/website', 'testdir/') to a directory. So this probably doesn't work on Windows. On *nix/Mac, however, the home directory ('~') is accounted for, so '~/projects/fixtures' would work.

### Instances
The *instances* attribute is used when building or destroying multiple copies of the same structure. It is a list whose default is ['local', 'remote']. Meaning under *parent*, the default strucure would produce

	local/
	      \
	       A/
	         \...
	remote/
		   \
		    A/
		      \...

This was really the point of the exercise for me, to have two copies to test migration, but I think it has other possibilities. 

## Installation
Sorry, not up on *pip* or *easy_install* yet, All the functionality is in dirfixtures.py. Also, tested in Python 2, haven't tried in Python 3.

** Warning: The default functionality is to add/remove directories and files in your current working directory. So playing with it within the DirFixtures directory should be fine; otherwise, make sure you don't have any directories named *A*, *remote*, or *local* or a file named *c.txt* in your current directory that you don't want overwritten. This is assuming you are using the defaults. If not, you're on your own.**

### Usage
## Getting started
Assuming you are in the DirFixture directory, 

	$ python
	>>> from dirfixtures import *
	>>> df = DirFixtures()
	>>> df.build()			# Creates default directory structure in current directory
	>>> df.destroy()		# Deletes that that directory structure
	>>> df.builds()			# Creates two instances of default structure under local and remote
	>>> df.destroys()		# Deletes local and remote directories from current directory

If you have another terminal or a GUI view of the directory of some sort, you should see an *A* diretory appear after the first command, build(); disappear after the second command, destroy(); directories *local* and *remote* appear after the third command, builds(); and disappear under the fourth, destroys().

## API
#Overriding the default *structure*, *parent*, and/or *instances* values
* When instantiating the object (`df = DirFixtures()`), you can pass in *structure*, *parent*, or *instances* to the object sequentially, `DirFixtures(structure, parent, instances)`, or via named values, e.g., `DirFixtures({ ... }, '...')` or `DirFixtures(parent='...')`
* These values can also be set and retrieved via properties, e.g., `df.strucure={ ... }` or `p = df.parent`
* Finally, the four core methods (build(), destroy(), builds(), destroys()) take a dict as their only argument and you can granularly override any of the above attributes via this syntax:

	df.build({ parent: '...', ... })

# Methods
* build() - creates *structure* under *parent*
* destroy() - deletes *structure* under *parent*
* builds() - creates instances of *structure* under each of the *instances* under *parent*
* destroys()  reverses `builds()`
* clone(path) - returns a *structure* based on an existing directory. 

Here's a more advanced usage example:

	$ python
	>>> from dirfixures import *
	>>> df = DirFixtures(parent='~/fixtures/')		# Create directories under fixtures directory
	>>> df.structure = df.clone('/var/www/html/website')	# Copy website into structure
	>>> df.builds()											# Build default local and remote instances
	[1]+  Stopped                 python
	$ ls ~/fixtures
	local  remote
	$ diff -rq ~/fixtures/local ~/fixtures/remote
	$ diff -rq ~/fixtures/local /var/www/html/website
	$ fg
	>>> df.destroys()										# Delete instances
	>>> quit()
	$ ls ~/fixtures
	$

My main purpose is to make the copies, modify one instance and then migrate the changes to the other to test unified-migration-theory, but I could see using it to create rails/yeoman style generators as well.

Hope you find this useful or inspiring or something.