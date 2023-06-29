# Makefile to update changelog using git-changelog

# Path to git-changelog executable
GIT_CHANGELOG = $(CONDA)/bin/git-changelog

# Path to Jinja template for changelog generation
CHANGELIST_TEMPLATE = path:./.maint/history.md.jinja

# Output file for the updated changelog
OUTPUT_FILE = docs/changes.md

# Target: Update the changelog
update_changelog:
	$(GIT_CHANGELOG) -bTrt $(CHANGELIST_TEMPLATE) -o $(OUTPUT_FILE)
