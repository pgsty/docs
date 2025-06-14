#!/usr/bin/env python3

import os
import psycopg2
from typing import Dict, List, Optional, Any

# Database connection
CONN = psycopg2.connect('postgres:///vonng')

# Global mappings for reverse dependency lookup and leading extensions
EXT_MAP = {}
DEP_MAP = {}
LEADING_MAP = {}  # Maps package names to leading extension names

# Constants
DEFAULT_OS = ['el8.x86_64', 'el8.aarch64', 'el9.x86_64', 'el9.aarch64', 'd12.x86_64', 'd12.aarch64', 'u22.x86_64', 'u22.aarch64', 'u24.x86_64', 'u24.aarch64']
DEFAULT_PG = [17, 16, 15, 14, 13]

# Directories
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..', 'content', 'ext', '(name)'))
STUB_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..', 'stub'))

# Utility functions
def normalize_arch(arch: str) -> str:
    """Normalize different architecture representations to standard format."""
    if not arch:
        return 'x86_64'  # default fallback
    
    arch = arch.lower().strip()
    
    # Map various x86_64 representations
    if arch in ['x86_64', 'amd64', 'x86', 'amd']:
        return 'x86_64'
    
    # Map various aarch64 representations  
    if arch in ['aarch64', 'arm64', 'arm', 'armv8']:
        return 'aarch64'
    
    # Return as-is if unknown, but log it
    print(f"Warning: Unknown architecture '{arch}', defaulting to x86_64")
    return 'x86_64'

def format_repo_badge(repo: str) -> str:
    """Format repository name as Badge component."""
    repo_badges = {
        'PGDG': '<Badge variant="blue-subtle"><span className="font-bold">PGDG</span></Badge>',
        'PIGSTY': '<Badge variant="amber-subtle"><span className="font-bold">PIGSTY</span></Badge>',
        'CONTRIB': '<Badge variant="green-subtle"><span className="font-bold">CONTRIB</span></Badge>',
        'MIXED': '<Badge variant="gray-subtle"><span className="font-bold">MIXED</span></Badge>'
    }
    return repo_badges.get(repo, f'<Badge variant="gray-subtle"><span className="font-bold">{repo}</span></Badge>' if repo else 'N/A')

def format_license_badge(license_name: str) -> str:
    """Format license as Badge component with appropriate color."""
    license_colors = {
        'PostgreSQL': 'blue-subtle',
        'BSD-0': 'blue-subtle', 'BSD 0-Clause': 'blue-subtle',
        'BSD-2': 'blue-subtle', 'BSD 2-Clause': 'blue-subtle', 
        'BSD-3': 'blue-subtle', 'BSD 3-Clause': 'blue-subtle',
        'MIT': 'teal-subtle', 'ISC': 'teal-subtle',
        'unrestricted': 'teal-subtle', 'Public': 'teal-subtle',
        'Artistic': 'green-subtle', 'Apache-2.0': 'green-subtle',
        'MPL-2.0': 'green-subtle', 'MPLv2': 'green-subtle',
        'GPL-2.0': 'pink-subtle', 'GPLv2': 'pink-subtle',
        'GPL-3.0': 'pink-subtle', 'GPLv3': 'pink-subtle',
        'LGPL-2.1': 'pink-subtle', 'LGPLv2': 'pink-subtle',
        'LGPL-3.0': 'pink-subtle', 'LGPLv3': 'pink-subtle',
        'AGPL-3.0': 'red-subtle', 'AGPLv3': 'red-subtle',
        'Timescale': 'gray-subtle'
    }
    variant = license_colors.get(license_name, 'gray-subtle')
    return f'<Badge variant="{variant}">{license_name}</Badge>'

def format_category_badge(category: str) -> str:
    """Format category as Badge component with icon."""
    category_icons = {
        'TIME': 'Clock',
        'GIS': 'Globe', 
        'RAG': 'Brain',
        'FTS': 'Search',
        'OLAP': 'ChartNoAxesCombined',
        'FEAT': 'Sparkles',
        'LANG': 'BookA',
        'TYPE': 'Boxes',
        'UTIL': 'Wrench',
        'FUNC': 'Variable',
        'ADMIN': 'Landmark',
        'STAT': 'Activity',
        'SEC': 'Shield',
        'FDW': 'FileInput',
        'SIM': 'Shell',
        'ETL': 'Truck'
    }
    icon = category_icons.get(category, 'Blocks')
    iconstr = '{<%s />}'% icon
    return f'<Badge icon={iconstr} variant="outline"><a href="/ext/{category.lower()}" className="no-underline">{category}</a></Badge>'

def format_pg_badge(pg_version: int, repo: str = '') -> str:
    """Format PostgreSQL version as Badge with appropriate color."""
    if repo == 'PIGSTY':
        return f'<Badge variant="amber-subtle">**PG{pg_version}**</Badge>'
    else:
        return f'<Badge variant="blue-subtle">**PG{pg_version}**</Badge>'

def parse_array(value: str) -> List[str]:
    """Parse PostgreSQL array string to Python list."""
    # already a list, return it
    if isinstance(value, list):
        return value
    if not value or not value.startswith('{') or not value.endswith('}'):
        return []
    return [item.strip() for item in value[1:-1].split(',') if item.strip()]

# Template for generating extension documentation
EXTENSION_TEMPLATE = '''---
title: {name}
description: {description}
full: true
---

import {{ File, Folder, Files }} from 'fumadocs-ui/components/files';
import {{ Package, Box }} from 'lucide-react';
import {{ Callout }} from 'fumadocs-ui/components/callout';
import {{ Badge }} from '@/components/ui/badge';
import {{ TooltipIconButton }} from '@/components/ui/tooltip-icon-button';
import {{
    Scale, Clock, Globe, Brain, Search, ChartNoAxesCombined,
    Sparkles, BookA, Boxes, Wrench, Variable, Landmark,
    Activity, Shield, FileInput, Shell, Truck, Blocks
}} from 'lucide-react';

## Overview

| <TooltipIconButton tooltip="Extension unique identifier" side="top">ID</TooltipIconButton> | <TooltipIconButton tooltip="Extension name" side="top">Name</TooltipIconButton> | <TooltipIconButton tooltip="Package name for installation" side="top">Package</TooltipIconButton> | <TooltipIconButton tooltip="Extension category" side="top">Category</TooltipIconButton> | <TooltipIconButton tooltip="Open source license" side="top">License</TooltipIconButton> | <TooltipIconButton tooltip="Official website or source code" side="top">Website</TooltipIconButton> | <TooltipIconButton tooltip="Programming language" side="top">Lang</TooltipIconButton> | <TooltipIconButton tooltip="Latest available extension version" side="top">Version</TooltipIconButton> |
|:--------:|:--------:|:----------:|:---------------------------------------:|:------------------------------------------------------:|:----------------------------------------------:|:----:|:--------------:|
| **{ext_id}** | {name_link} | {package} | {category_badge} | {license_badge} | [Source]({url}) | {language} | {version} |

### Attributes

| <TooltipIconButton tooltip="The Primary Leading extension in the Package" side="top">Leading</TooltipIconButton> | <TooltipIconButton tooltip="Contains binary utils" side="top">Has Bin</TooltipIconButton> | <TooltipIconButton tooltip="Contains .so shared library files" side="top">Has Lib</TooltipIconButton> | <TooltipIconButton tooltip="Requires preloading via shared_preload_libraries" side="top">PreLoad</TooltipIconButton> | <TooltipIconButton tooltip="Requires CREATE EXTENSION DDL command" side="top">Need DDL</TooltipIconButton> | <TooltipIconButton tooltip="Can be installed in any schema" side="top">Relocatable</TooltipIconButton> | <TooltipIconButton tooltip="Can be created by non-superuser" side="top">Trusted</TooltipIconButton> | <TooltipIconButton tooltip="Schemas used by this extension" side="top">Schemas</TooltipIconButton> |
|:-------:|:-------:|:-------:|:-------:|:--------:|:-----------:|:-------:|:-------:|
| {lead} | {has_bin} | {has_lib} | {need_load} | {need_ddl} | {relocatable} | {trusted} | {schemas} |

### Packages

| <TooltipIconButton tooltip="Linux distribution family, EL or Debian" side="top">Distro</TooltipIconButton> | <TooltipIconButton tooltip="Package repository" side="top">Repo</TooltipIconButton> | <TooltipIconButton tooltip="The RPM/DEB Package Name Pattern (replace $v with real pg major)" side="top">Package Name</TooltipIconButton> | <TooltipIconButton tooltip="Latest package version" side="top">Version</TooltipIconButton> | <TooltipIconButton tooltip="RPM/DEB Package dependencies" side="top">Deps</TooltipIconButton> | <TooltipIconButton tooltip="Available in these PostgreSQL Major Versions" side="top">PG Major</TooltipIconButton> |
|:----------:|:--------:|:------------------------:|:-----------:|:------------:|:------------------:|
{package_info}

{dependencies_section}

------

## Availability

{availability_table}

<Badge variant="green-subtle"><span className="font-black">CONTRIB</span></Badge> <Badge variant="blue-subtle"><span className="font-black">PGDG</span></Badge> <Badge variant="amber-subtle"><span className="font-black">PIGSTY</span></Badge>

------

## Download

{download_section}

------

## Install

{install_section}

{stub_content}
'''


class Package:
    """Represents a PostgreSQL extension package."""
    
    def __init__(self, row):
        (self.pkg, self.pname, self.os, self.pg, self.name, self.ver, self.org, 
         self.type, self.os_code, self.os_arch, self.repo, self.version, 
         self.release, self.file, self.sha256, self.url, self.mirror_url, 
         self.size, self.size_full) = row
    
    def __str__(self):
        return f"{self.pname} @ {self.os}"



class Extension:
    """Represents a PostgreSQL extension with all its metadata and packages."""
    
    def __init__(self, row):
        # Unpack the database row
        (self.id, self.name, self.pkg, self.alias, self.category, self.state, 
         self.url, self.license, self.tags, self.version, self.repo, self.lang, 
         self.contrib, self.lead, self.has_bin, self.has_lib, self.need_ddl, 
         self.need_load, self.trusted, self.relocatable, self.schemas, 
         self.pg_ver, self.requires, self.rpm_ver, self.rpm_repo, self.rpm_pkg, 
         self.rpm_pg, self.rpm_deps, self.deb_ver, self.deb_repo, self.deb_pkg, 
         self.deb_deps, self.deb_pg, self.bad_case, self.extra, self.ctime, 
         self.mtime, self.en_desc, self.zh_desc, self.comment) = row
        
        # Parse array fields
        self.tags = parse_array(self.tags) if self.tags else []
        self.pg_ver = parse_array(self.pg_ver) if self.pg_ver else []
        self.requires = parse_array(self.requires) if self.requires else []
        self.schemas = parse_array(self.schemas) if self.schemas else []
        self.rpm_deps = parse_array(self.rpm_deps) if self.rpm_deps else []
        self.deb_deps = parse_array(self.deb_deps) if self.deb_deps else []
        self.rpm_pg = parse_array(self.rpm_pg) if self.rpm_pg else []
        self.deb_pg = parse_array(self.deb_pg) if self.deb_pg else []
        
        # Computed properties
        self.has_rpm = bool(self.rpm_repo)
        self.has_deb = bool(self.deb_repo)
        self.packages: List[Package] = []
    
    def __str__(self):
        return self.name
    
    def load_packages(self):
        """Load package information from database."""
        with CONN.cursor() as cur:
            cur.execute('SELECT * FROM ext.pkg WHERE pkg = %s ORDER BY type DESC, os, pg DESC;', (self.pkg,))
            res = cur.fetchall()
        self.packages = [Package(row) for row in res]

    def format_bool(self, value: Optional[bool], true_text: str = "Yes", false_text: str = "No") -> str:
        """Format boolean value for display."""
        if value is None:
            return "Unknown"
        return true_text if value else false_text
    
    def generate_dependencies_section(self) -> str:
        """Generate dependencies, reverse dependencies, and comments callout sections."""
        sections = []
        
        # Dependencies (what this extension requires)
        if self.requires:
            deps_links = [f"[{dep}](/ext/{dep})" for dep in self.requires]
            deps_text = ", ".join(deps_links)
            sections.append(f'''
<Callout title="Dependencies" type="warn">
    This extension depends on: {deps_text}
</Callout>
''')
        
        # Reverse dependencies (what depends on this extension)
        if self.name in DEP_MAP:
            dependents = DEP_MAP[self.name]
            dependent_links = [f"[{dep}](/ext/{dep})" for dep in dependents]
            dependent_text = ", ".join(dependent_links)
            sections.append(f'''
<Callout title="Dependent Extensions" type="info">
    The following extensions depend on this extension: {dependent_text}
</Callout>
''')
        
        # Comments (if extension has comment field)
        if self.comment and self.comment.strip():
            sections.append(f'''
<Callout title="Comments" type="info">
    {self.comment}
</Callout>
''')
        
        return ''.join(sections)
    
    def generate_package_info(self) -> str:
        """Generate package information table rows."""
        rows = []
        
        if self.has_rpm:
            rpm_pg_versions = ", ".join(map(str, self.rpm_pg)) if self.rpm_pg else "-"
            rpm_deps = "<br /> ".join([ '`%s`'%i for i in self.rpm_deps]) if self.rpm_deps else "-"
            rows.append(f"|   **EL**   | {format_repo_badge(self.rpm_repo)} | `{self.rpm_pkg or '-'}` | `{self.rpm_ver or '-'}` | {rpm_deps} | {rpm_pg_versions} |")
            
        if self.has_deb:
            deb_pg_versions = ", ".join(map(str, self.deb_pg)) if self.deb_pg else "-"
            deb_deps = "<br /> ".join([ '`%s`'%i for i in self.deb_deps]) if self.deb_deps else "-"
            rows.append(f"| **Debian** | {format_repo_badge(self.deb_repo)} | `{self.deb_pkg or '-'}` | `{self.deb_ver or '-'}` | {deb_deps} | {deb_pg_versions} |")
        
        return "\n".join(rows) if rows else "| - | - | - | - | - | - |"
    
    def generate_availability_table(self) -> str:
        """Generate availability matrix table with merged Linux column and Badge components."""
        self.load_packages()
        
        # Build package matrix with repository information using new DEFAULT_OS format
        matrix = {}
        repo_matrix = {}
        for os in DEFAULT_OS:
            matrix[os] = {}
            repo_matrix[os] = {}
            for pg in DEFAULT_PG:
                matrix[os][pg] = ""
                repo_matrix[os][pg] = ""
        
        # Fill matrix with package versions and repository info
        for pkg in self.packages:
            # Convert package OS info to DEFAULT_OS format for matching
            pkg_os_code = getattr(pkg, 'os_code', getattr(pkg, 'os', '').split('.')[0])
            pkg_arch = normalize_arch(getattr(pkg, 'os_arch', ''))
            pkg_os_key = f"{pkg_os_code}.{pkg_arch}"
            
            if pkg_os_key in matrix and pkg.pg in matrix[pkg_os_key]:
                matrix[pkg_os_key][pkg.pg] = pkg.version
                repo_matrix[pkg_os_key][pkg.pg] = pkg.org.upper()
        
        # Generate PG version headers based on extension support
        pg_headers = []
        for pg in DEFAULT_PG:
            if str(pg) in self.pg_ver:
                pg_headers.append(f'**PG{pg}**')  # Normal text for supported versions
            else:
                pg_headers.append(f'<span className="text-red-500">**PG{pg}**</span>')  # Red for unsupported versions
        
        # Generate table with merged Linux column
        headers = ['<TooltipIconButton tooltip="Linux Distro Arch / PostgreSQL Major Version" side="top">Linux / PostgreSQL </TooltipIconButton>'] + pg_headers
        rows = [f"| {' | '.join(headers)} |"]
        rows.append(f"|{'|'.join([':-----:'] * len(headers))}|")
        
        for os in DEFAULT_OS:
            # DEFAULT_OS is now in format 'el8.x86_64', 'el8.aarch64', etc.
            linux_cell = f'`{os}`'
            
            row_data = [linux_cell]
            for pg in DEFAULT_PG:
                version = matrix[os][pg]
                repo = repo_matrix[os][pg]
                if version:
                    if repo == 'PIGSTY':
                        row_data.append(f'<Badge variant="amber-subtle">{version}</Badge>')
                    elif repo == 'PGDG':
                        row_data.append(f'<Badge variant="blue-subtle">{version}</Badge>')
                    elif repo == 'CONTRIB':
                        row_data.append(f'<Badge variant="green-subtle">{version}</Badge>')
                    else:
                        row_data.append(f'<Badge variant="purple-subtle">{version}</Badge>')

                elif self.contrib:
                    if str(pg) in self.pg_ver:
                        row_data.append('<Badge variant="green-subtle">%s</Badge>'% self.version)
                    else:
                        row_data.append('<Badge variant="red-subtle">✗</Badge>')
                else:
                    row_data.append('<Badge variant="red-subtle">✗</Badge>')
            
            rows.append(f"| {' | '.join(row_data)} |")
        
        return "\n".join(rows)
    
    def generate_download_section(self) -> str:
        """Generate download section with file tree using actual package names from database."""
        if self.contrib:
            return "This extension is built-in with PostgreSQL and does not need separate download."
        
        repo_text = format_repo_badge(self.rpm_repo or self.deb_repo or 'Unknown')
        
        section = f"""To add the required PGDG / PIGSTY upstream repository, use:

```bash tab="pig"
pig repo add pgdg -u    # add PGDG repo and update cache (leave existing repos)
pig repo add pigsty -u  # add PIGSTY repo and update cache (leave existing repos)
pig repo add pgsql -u   # add PGDG + Pigsty repo and update cache (leave existing repos)
pig repo set all -u     # set repo to all = NODE + PGSQL + INFRA  (remove existing repos)
```
```bash tab="pigsty"
./node.yml -t node_repo -e node_repo_modules=node,pgsql # -l <cluster>
```

Or download the latest packages directly:

<Files>"""

        # Load actual package data from database
        self.load_packages()
        
        # Group packages by OS/architecture with proper normalization
        pkg_by_os = {}
        for pkg in self.packages:
            # Create standardized OS key using normalize_arch for consistent matching
            os_code = getattr(pkg, 'os_code', getattr(pkg, 'os', '').split('.')[0])
            normalized_arch = normalize_arch(getattr(pkg, 'os_arch', ''))
            os_key = f"{os_code}.{normalized_arch}"
            
            if os_key not in pkg_by_os:
                pkg_by_os[os_key] = {}
            pkg_by_os[os_key][pkg.pg] = pkg
        
        
        # Generate file tree for each OS
        for os in DEFAULT_OS:
            # Parse the new DEFAULT_OS format (e.g., 'el8.x86_64')
            os_parts = os.split('.')
            if len(os_parts) != 2:
                print(f"Warning: Invalid OS format '{os}', skipping")
                continue
                
            os_name = os_parts[0]
            arch = os_parts[1]  # Already in correct format (x86_64 or aarch64)
            
            section += f"""
    <Folder name="{os_name}.{arch}">"""
            
            # Look for packages for this OS/arch combination  
            os_key = f"{os_name}.{arch}"
            found_packages = False
            
            # Try exact match, then fuzzy matching
            search_keys = [os_key] + [key for key in pkg_by_os if key.endswith(f'.{arch}') and key.startswith(os_name)]
            
            for search_key in search_keys:
                if search_key in pkg_by_os:
                    for pg in DEFAULT_PG:
                        if str(pg) in self.pg_ver and pg in pkg_by_os[search_key]:
                            pkg = pkg_by_os[search_key][pg]
                            found_packages = True
                            
                            # Use actual package data from database
                            file_name = getattr(pkg, 'file', f'{self.name}-{pkg.version}.rpm')
                            url = getattr(pkg, 'url', '#')
                            
                            # Determine icon and color based on distro and architecture
                            icon_name = "Package" if os_name.startswith(('el', 'rocky', 'alma')) else "Box"
                            icon_color = "text-emerald-500" if arch == 'x86_64' else "text-orange-500"
                            
                            section += f"""
        <a href="{url}"><File name="{file_name}" icon={{<{icon_name} className="{icon_color}" />}} /></a>"""
                    if found_packages:
                        break
            
            section += """
    </Folder>"""
        
        section += """
</Files>"""
        
        return section
    
    def generate_install_section(self) -> str:
        """Generate installation instructions."""
        if self.contrib:
            install_text = f"""Extension `{self.name}` is PostgreSQL Built-in [**Contrib**](/ext/list/contrib) Extension which is installed along with the kernel/contrib.

[**Create**](/docs/pgsql/extension/create) this extension on PostgreSQL database with:

```sql
CREATE EXTENSION {self.name};
```"""
        else:
            install_text = f"""[**Install**](/docs/pgsql/extension/install) this extension with:

```bash tab="pig"
pig ext install {self.name}; 	    # install by extension name, for the current active PG version
"""
            if self.pkg != self.name:
                install_text += f"""
pig ext install {self.pkg}; 	    # install via package alias, for the active PG version"""

            for pg in DEFAULT_PG:
                if str(pg) in self.pg_ver:
                    install_text += f"""
pig ext install {self.name} -v {pg};   # install for PG {pg}"""
            
            install_text += """
```"""
            
            if self.has_rpm:
                install_text += """
```bash tab="yum" """
                for pg in DEFAULT_PG:
                    if str(pg) in self.pg_ver:
                        # Fix package name without wildcards
                        if '$v' in self.rpm_pkg:
                            pkg_name = self.rpm_pkg.replace('$v', str(pg))
                        else:
                            pkg_name = self.rpm_pkg
                        install_text += f"""
dnf install {pkg_name};"""
                install_text += """
```"""
            
            if self.has_deb:
                install_text += """
```bash tab="apt" """
                for pg in DEFAULT_PG:
                    if str(pg) in self.pg_ver:
                        # Fix package name without wildcards
                        if '$v' in self.deb_pkg:
                            pkg_name = self.deb_pkg.replace('$v', str(pg))
                        else:
                            pkg_name = f"postgresql-{pg}-{self.deb_pkg}"
                        install_text += f"""
apt install {pkg_name};"""
                install_text += """
```"""
            
            install_text += f"""
```bash tab="ansible"
./pgsql.yml -t pg_ext -e '{{"pg_extensions": ["{self.pkg}"]}}' # -l <cls>
```"""

            if self.need_load:
                install_text += f"""

[**Preload**](/docs/pgsql/extension/load) this extension with `shared_preload_libraries`:

```bash
shared_preload_libraries = '{self.name}'; # add to pg cluster config
```"""

            if self.need_ddl:
                create_cmd = f'"{self.name}"' if '-' in self.name else self.name
                cascade = ' CASCADE' if self.requires else ''
                install_text += f"""

[**Create**](/docs/pgsql/extension/create) this extension with:

```sql
CREATE EXTENSION {create_cmd}{cascade};
```"""
            else:
                install_text += f"""

Extension `{self.name}` [**does not need**](/docs/pgsql/extension/create#list-of-extensions-without-ddl) `CREATE EXTENSION` command."""
        
        return install_text
    
    def load_stub_content(self) -> str:
        """Load additional stub content for the extension."""
        stub_path = os.path.join(STUB_DIR, f"{self.name}.md")
        if os.path.exists(stub_path):
            with open(stub_path, 'r') as f:
                return f.read()
        return ""
    
    def generate_documentation(self) -> str:
        """Generate complete MDX documentation for the extension."""
        # Format template variables with improved name and package linking
        name_link = f'[`{self.name}`]({self.url})' if self.url else f'`{self.name}`'
        
        # Package linking logic: link to leading extension if pkg != name
        if self.pkg != self.name and self.pkg in LEADING_MAP:
            leading_ext = LEADING_MAP[self.pkg]
            package_link = f'[`{self.pkg}`](/ext/{leading_ext})'
        else:
            package_link = f'`{self.pkg}`'
        
        template_vars = {
            'name': self.name,
            'name_link': name_link,
            'description': self.en_desc or 'PostgreSQL Extension',
            'ext_id': self.id,
            'package': package_link,
            'category': self.category,
            'category_lower': self.category.lower(),
            'category_badge': format_category_badge(self.category),
            'license_badge': format_license_badge(self.license),
            'url': self.url or '#',
            'language': self.lang or 'Unknown',
            'version': self.version or 'Unknown',
            'lead': self.format_bool(self.lead),
            'has_bin': self.format_bool(self.has_bin),
            'has_lib': self.format_bool(self.has_lib),
            'need_load': self.format_bool(self.need_load),
            'need_ddl': self.format_bool(self.need_ddl),
            'relocatable': self.format_bool(self.relocatable),
            'trusted': self.format_bool(self.trusted),
            'schemas': ', '.join(f'`{s}`' for s in self.schemas) if self.schemas else '-',
            'package_info': self.generate_package_info(),
            'dependencies_section': self.generate_dependencies_section(),
            'availability_table': self.generate_availability_table(),
            'download_section': self.generate_download_section(),
            'install_section': self.generate_install_section(),
            'stub_content': self.load_stub_content()
        }
        
        return EXTENSION_TEMPLATE.format(**template_vars)
    
    def save_documentation(self):
        """Save the generated documentation to file."""
        content = self.generate_documentation()
        output_path = os.path.join(OUTPUT_DIR, f"{self.name}.mdx")
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)

def build_leading_extension_map(extensions: List['Extension']) -> Dict[str, str]:
    """Build a mapping from package names to their leading extensions."""
    leading_map = {}
    for ext in extensions:
        if ext.lead and ext.pkg:  # This is a leading extension
            leading_map[ext.pkg] = ext.name
    return leading_map

def main():
    """Main function to generate documentation for all extensions."""
    print("Loading extensions from database...")
    
    with CONN.cursor() as cur:
        cur.execute('SELECT * FROM ext.extension ORDER BY id')
        rows = cur.fetchall()
    
    extensions = [Extension(row) for row in rows]
    
    # Build global dependency and leading extension maps
    print("Building dependency and leading extension maps...")
    global EXT_MAP, DEP_MAP, LEADING_MAP
    LEADING_MAP = build_leading_extension_map(extensions)
    
    for ext in extensions:
        EXT_MAP[ext.name] = ext
        if ext.requires:
            for req in ext.requires:
                if req not in DEP_MAP:
                    DEP_MAP[req] = []
                DEP_MAP[req].append(ext.name)
    
    print(f"Found {len(extensions)} extensions.")
    print(f"Found {len(LEADING_MAP)} leading extensions.")
    print("Generating documentation...")
    
    for ext in extensions:
        try:
            print(f"Processing {ext.name}...")
            ext.save_documentation()
        except Exception as e:
            print(f"Error processing {ext.name}: {e}")
    
    print("Documentation generation complete!")


if __name__ == "__main__":
    main()
