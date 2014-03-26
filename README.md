#ScaffoldDirs

The point of this module is to easily create, delete, and copy directory structures. It came about because of the larger goal of my [unified-migration-theory](https://github.com/athill/unified-migration-theory) project, which got stonewalled when I discovered the difficulty of maintaining test directories manually.

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

Each key has a *type* attribute that is either *file* or *dir*. File types have an optional content attribute with the contents of the file. Dir types have an optional *children* attribute, that mirrors the parent structure. 

	A/
	  \
	   B/
	     \_a.txt
	     |
	     |_b.txt
	c.txt

### Parent
Parent is where to build the directory structure(s). The default is the current directory. It's a string and expects a *nix path (e.g., '/var/www/html/website', 'testdir/') to a directory. So this probably doesn't work on Windows. On *nix/Mac, however, the home directory ('~') is accounted for, so '~/projects/fixtures' would work.