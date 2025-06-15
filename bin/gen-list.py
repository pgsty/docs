#!/usr/bin/env python3

import os
import psycopg2
from typing import Dict, List, Optional, Any
from collections import defaultdict, Counter

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
OUTPUT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..', 'content', 'ext', 'list'))

# Category metadata
CATEGORY_META = {
    "TIME": {
        "description": "TimescaleDB, Versioning & Temporal Table, Crontab, Async & Background Job Scheduler",
        "icon": "Clock",
        "color": "blue-subtle"
    },
    "GIS": {
        "description": "GeoSpatial Data Types, Operators, and Indexes, Hexagonal Indexing, OGR Data FDW, GeoIP & MobilityDB",
        "icon": "Globe",
        "color": "green-subtle"
    },
    "RAG": {
        "description": "Vector Database with IVFFLAT, HNSW, DiskANN Indexes, AI & ML in SQL interface, Similarity Funcs",
        "icon": "Brain",
        "color": "purple-subtle"
    },
    "FTS": {
        "description": "ElasticSearch Alternative with BM25, 2-gram/3-gram Fuzzy Search, Zhparser & Hunspell Segregation Dicts",
        "icon": "Search",
        "color": "amber-subtle"
    },
    "OLAP": {
        "description": "DuckDB Integration with FDW & PG Lakehouse, Access Parquet from File/S3, Sharding with Citus/Partman/PlProxy",
        "icon": "ChartNoAxesCombined",
        "color": "red-subtle"
    },
    "FEAT": {
        "description": "OpenCypher with AGE, GraphQL, JsonSchema, Hints & Hypo Index, HLL, Rum, IVM, ChemRDKit, and Message Queues",
        "icon": "Sparkles",
        "color": "pink-subtle"
    },
    "LANG": {
        "description": "Develop, Test, Package, and Deliver Stored Procedures written in various PL/Languages: Java, Js, Lua, R, Sh, PRQL",
        "icon": "BookA",
        "color": "teal-subtle"
    },
    "TYPE": {
        "description": "Dedicate New Data Types Like: prefix, sember, uint, SIUnit, RoaringBitmap, Rational, Sphere, Hash, RRule",
        "icon": "Boxes",
        "color": "gray-subtle"
    },
    "UTIL": {
        "description": "Utilities such as send http request, perform gzip/zstd compress, send mails, Regex, ICU, encoding, docs, Encryption",
        "icon": "Wrench",
        "color": "amber-subtle"
    },
    "FUNC": {
        "description": "Function such as id generator, aggregations, sketches, vector functions, mathematical functions and digest functions",
        "icon": "Variable",
        "color": "pink-subtle"
    },
    "ADMIN": {
        "description": "Utilities for Bloat Control, DirtyRead, BufferInspect, DDL Generate, ChecksumVerify, Permission, Priority, Catalog",
        "icon": "Landmark",
        "color": "gray-subtle"
    },
    "STAT": {
        "description": "Observability Catalogs, Monitoring Metrics & Views, Statistics, Query Plans, WaitSampling, SlowLogs",
        "icon": "Activity",
        "color": "green-subtle"
    },
    "SEC": {
        "description": "Auditing Logs, Enforce Passwords, Keep Secrets, TDE, SM Algorithm, Login Hooks, Log Erros, Extension White List",
        "icon": "Shield",
        "color": "red-subtle"
    },
    "FDW": {
        "description": "Wrappers & Multicorn for FDW Development, Access other DBMS: MySQL, Mongo, SQLite, MSSQL, Oracle, HDFS, DB2",
        "icon": "FileInput",
        "color": "blue-subtle"
    },
    "SIM": {
        "description": "Protocol Simulation & heterogeneous DBMS Compatibility: Oracle, MSSQL, DB2, MySQL, Memcached, and Babelfish",
        "icon": "Shell",
        "color": "teal-subtle"
    },
    "ETL": {
        "description": "Logical Replication, Decoding, CDC in protobuf/JSON/Mongo format, Copy & Load & Compare Postgres Databases",
        "icon": "Truck",
        "color": "purple-subtle"
    }
}

# Utility functions from gen-ext.py
def parse_array(value: str) -> List[str]:
    """Parse PostgreSQL array string to Python list."""
    if isinstance(value, list):
        return value
    if not value or not value.startswith('{') or not value.endswith('}'):
        return []
    return [item.strip() for item in value[1:-1].split(',') if item.strip()]

def format_category_badge(category: str) -> str:
    """Format category as Badge component with icon and color."""
    meta = CATEGORY_META.get(category, {'icon': 'Blocks', 'color': 'gray-subtle'})
    iconstr = '{<%s />}' % meta['icon']
    return f'<Badge icon={iconstr} variant="{meta["color"]}"><a href="/ext/{category.lower()}" className="no-underline">{category}</a></Badge>'

def format_license_badge(license_name: str) -> str:
    """Format license as Badge component with standard colors and links."""
    # License mapping to standard names and anchor links
    license_mapping = {
        'PostgreSQL': {'name': 'PostgreSQL', 'anchor': 'postgresql', 'variant': 'blue-subtle'},
        'MIT': {'name': 'MIT', 'anchor': 'mit', 'variant': 'blue-subtle'},
        'ISC': {'name': 'ISC', 'anchor': 'isc', 'variant': 'blue-subtle'},
        'BSD-0': {'name': 'BSD 0-Clause', 'anchor': 'bsd-0-clause', 'variant': 'blue-subtle'},
        'BSD 0-Clause': {'name': 'BSD 0-Clause', 'anchor': 'bsd-0-clause', 'variant': 'blue-subtle'},
        'BSD-2': {'name': 'BSD 2-Clause', 'anchor': 'bsd-2-clause', 'variant': 'blue-subtle'},
        'BSD 2-Clause': {'name': 'BSD 2-Clause', 'anchor': 'bsd-2-clause', 'variant': 'blue-subtle'},
        'BSD-3': {'name': 'BSD 3-Clause', 'anchor': 'bsd-3-clause', 'variant': 'blue-subtle'},
        'BSD 3-Clause': {'name': 'BSD 3-Clause', 'anchor': 'bsd-3-clause', 'variant': 'blue-subtle'},
        'Artistic': {'name': 'Artistic', 'anchor': 'artistic', 'variant': 'green-subtle'},
        'Apache-2.0': {'name': 'Apache-2.0', 'anchor': 'apache-20', 'variant': 'green-subtle'},
        'MPL-2.0': {'name': 'MPL-2.0', 'anchor': 'mpl-20', 'variant': 'green-subtle'},
        'MPLv2': {'name': 'MPL-2.0', 'anchor': 'mpl-20', 'variant': 'green-subtle'},
        'GPL-2.0': {'name': 'GPL-2.0', 'anchor': 'gpl-20', 'variant': 'amber-subtle'},
        'GPLv2': {'name': 'GPL-2.0', 'anchor': 'gpl-20', 'variant': 'amber-subtle'},
        'GPL-3.0': {'name': 'GPL-3.0', 'anchor': 'gpl-30', 'variant': 'amber-subtle'},
        'GPLv3': {'name': 'GPL-3.0', 'anchor': 'gpl-30', 'variant': 'amber-subtle'},
        'LGPL-2.1': {'name': 'LGPL-2.1', 'anchor': 'lgpl-21', 'variant': 'amber-subtle'},
        'LGPLv2': {'name': 'LGPL-2.1', 'anchor': 'lgpl-21', 'variant': 'amber-subtle'},
        'LGPL-3.0': {'name': 'LGPL-3.0', 'anchor': 'lgpl-30', 'variant': 'amber-subtle'},
        'LGPLv3': {'name': 'LGPL-3.0', 'anchor': 'lgpl-30', 'variant': 'amber-subtle'},
        'AGPL-3.0': {'name': 'AGPL-3.0', 'anchor': 'agpl-30', 'variant': 'red-subtle'},
        'AGPLv3': {'name': 'AGPL-3.0', 'anchor': 'agpl-30', 'variant': 'red-subtle'},
        'Timescale': {'name': 'Timescale', 'anchor': 'timescale', 'variant': 'gray-subtle'}
    }
    
    license_info = license_mapping.get(license_name, {
        'name': license_name, 
        'anchor': license_name.lower().replace(' ', '-').replace('.', ''), 
        'variant': 'gray-subtle'
    })
    
    return f'<a href="/ext/list/license#{license_info["anchor"]}" className="no-underline"><Badge icon={{<Scale />}} variant="{license_info["variant"]}">{license_info["name"]}</Badge></a>'

def format_language_badge(language: str) -> str:
    """Format programming language as Badge component with appropriate color."""
    language_dict = {
        'Python': { "variant": 'blue-subtle'   ,"anchor": "/ext/list/lang#python" },
        'Rust':   { "variant": 'amber-subtle'  ,"anchor": "/ext/list/lang#rust" },
        'SQL':    { "variant": 'green-subtle'  ,"anchor": "/ext/list/lang#sql" },
        'Java':   { "variant": 'pink-subtle'   ,"anchor": "/ext/list/lang#java" },
        'Data':   { "variant": 'teal-subtle'   ,"anchor": "/ext/list/lang#data" },
        'C++':    { "variant": 'purple-subtle' ,"anchor": "/ext/list/lang#c-1" },
        'C':      { "variant": 'blue-subtle'   ,"anchor": "/ext/list/lang#c" },
    }
    info = language_dict.get(language, 'gray-subtle')
    return f'<a href="{info['anchor']}"><Badge icon={{<FileCode2 />}} variant="{info['variant']}">{language or "N/A"}</Badge></a>'

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

def generate_simple_extension_table(extensions: List['Extension']) -> str:
    """Generate simple extension table (ID, Name, Package, Description)."""
    if not extensions:
        return "No extensions found."
    
    headers = ['ID', 'Extension', 'Package', 'Description']
    header_row = '| ' + ' | '.join(headers) + ' |'
    separator_row = '|:---:|:---|:---|:---|'
    
    rows = [header_row, separator_row]
    
    for ext in extensions:
        package_cell = f'[`{ext.pkg}`](/ext/{LEADING_MAP[ext.pkg]})'
        row_data = [
            str(ext.id),
            f'[`{ext.name}`](/ext/{ext.name})',
            package_cell,
            ext.en_desc or 'No description'
        ]
        rows.append('| ' + ' | '.join(row_data) + ' |')
    
    return '\n'.join(rows)

def generate_category_extension_table(extensions: List['Extension']) -> str:
    """Generate extension table for category lists (ID, Name, Package, Version, Description)."""
    if not extensions:
        return "No extensions found."
    
    headers = ['ID', 'Extension', 'Package', 'Version', 'Description']
    header_row = '| ' + ' | '.join(headers) + ' |'
    separator_row = '|:---:|:---|:---|:---|:---|'
    
    rows = [header_row, separator_row]
    
    for ext in extensions:
        package_cell = f'[`{ext.pkg}`](/ext/{LEADING_MAP[ext.pkg]})'
        row_data = [
            str(ext.id),
            f'[`{ext.name}`](/ext/{ext.name})',
            package_cell,
            ext.version or 'N/A',
            ext.en_desc or 'No description'
        ]
        rows.append('| ' + ' | '.join(row_data) + ' |')
    
    return '\n'.join(rows)

def build_leading_extension_map(extensions: List['Extension']) -> Dict[str, str]:
    """Build a mapping from package names to their leading extensions."""
    leading_map = {}
    for ext in extensions:
        if ext.lead and ext.pkg:  # This is a leading extension
            leading_map[ext.pkg] = ext.name
    return leading_map

def load_extensions() -> List['Extension']:
    """Load all extensions from database."""
    print("Loading extensions from database...")
    
    with CONN.cursor() as cur:
        cur.execute('SELECT * FROM ext.extension ORDER BY id')
        rows = cur.fetchall()
    
    extensions = [Extension(row) for row in rows]
    
    # Build global dependency and leading extension maps
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
    return extensions

def gen_category_list(extensions: List['Extension']):
    """Generate By Category list (content/ext/list/cate.mdx)."""
    print("Generating category list...")
    
    # Group extensions by category
    category_groups = defaultdict(list)
    for ext in extensions:
        category_groups[ext.category].append(ext)
    
    # Generate category overview table
    category_table_rows = []
    for category in CATEGORY_META.keys():
        count = len(category_groups[category])
        meta = CATEGORY_META[category]
        category_table_rows.append(f'| {format_category_badge(category)} | {count} | {meta["description"]} |')
    
    category_overview_table = f'''| Category | Count | Description |
|:---------|:-----:|:------------|
{chr(10).join(category_table_rows)}'''
    
    # Generate category sections
    category_sections = []
    for category in CATEGORY_META.keys():
        if category not in category_groups:
            continue
        
        cat_extensions = sorted(category_groups[category], key=lambda e: e.name)
        count = len(cat_extensions)
        meta = CATEGORY_META[category]
        
        section = f'''
## {category}

{meta["description"]}

{format_category_badge(category)} <Badge variant="gray-subtle">{count} Extensions</Badge>

{generate_category_extension_table(cat_extensions)}
'''
        category_sections.append(section)
    
    content = f'''---
title: By Category
description: PostgreSQL extensions organized by functionality categories
icon: Shapes
full: true
---

import {{ Badge }} from '@/components/ui/badge';
import {{ Clock, Globe, Brain, Search, ChartNoAxesCombined, Sparkles, BookA, Boxes, Wrench, Variable, Landmark, Activity, Shield, FileInput, Shell, Truck }} from 'lucide-react';

<Badge icon={{<Clock />}}               variant="blue-subtle"><a   href="#time" className="no-underline">TIME</a></Badge>
<Badge icon={{<Globe />}}               variant="green-subtle"><a  href="#gis" className="no-underline">GIS</a></Badge>
<Badge icon={{<Brain />}}               variant="purple-subtle"><a href="#rag" className="no-underline">RAG</a></Badge>
<Badge icon={{<Search />}}              variant="amber-subtle"><a  href="#fts" className="no-underline">FTS</a></Badge>
<Badge icon={{<ChartNoAxesCombined />}} variant="red-subtle"><a    href="#olap" className="no-underline">OLAP</a></Badge>
<Badge icon={{<Sparkles />}}            variant="pink-subtle"><a   href="#feat" className="no-underline">FEAT</a></Badge>
<Badge icon={{<BookA />}}               variant="teal-subtle"><a   href="#lang" className="no-underline">LANG</a></Badge>
<Badge icon={{<Boxes />}}               variant="gray-subtle"><a   href="#type" className="no-underline">TYPE</a></Badge><br />
<Badge icon={{<Wrench />}}              variant="amber-subtle"><a  href="#util" className="no-underline">UTIL</a></Badge>
<Badge icon={{<Variable />}}            variant="pink-subtle"><a   href="#func" className="no-underline">FUNC</a></Badge>
<Badge icon={{<Landmark />}}            variant="gray-subtle"><a   href="#admin" className="no-underline">ADMIN</a></Badge>
<Badge icon={{<Activity />}}            variant="green-subtle"><a  href="#stat" className="no-underline">STAT</a></Badge>
<Badge icon={{<Shield />}}              variant="red-subtle"><a    href="#sec" className="no-underline">SEC</a></Badge>
<Badge icon={{<FileInput />}}           variant="blue-subtle"><a   href="#fdw" className="no-underline">FDW</a></Badge>
<Badge icon={{<Shell />}}               variant="teal-subtle"><a   href="#sim" className="no-underline">SIM</a></Badge>
<Badge icon={{<Truck />}}               variant="purple-subtle"><a href="#etl" className="no-underline">ETL</a></Badge>

## Summary

{category_overview_table}

{''.join(category_sections)}
'''
    
    output_path = os.path.join(OUTPUT_DIR, 'cate.mdx')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Generated: {output_path}")

def gen_linux_distro_list(extensions: List['Extension']):
    """Generate By Linux list (content/ext/list/linux.mdx)."""
    print("Generating Linux distro list...")
    
    # Load packages to analyze OS support
    all_packages = []
    with CONN.cursor() as cur:
        cur.execute('SELECT * FROM ext.pkg ORDER BY os, pg DESC')
        rows = cur.fetchall()
    all_packages = [Package(row) for row in rows]
    
    # Group by OS
    os_groups = defaultdict(set)
    for pkg in all_packages:
        os_key = f"{pkg.os_code}.{pkg.os_arch}"
        os_groups[os_key].add(pkg.pkg)
    
    # Generate OS sections
    os_sections = []
    os_map = {
        'el8': 'Enterprise Linux 8 (RHEL 8, CentOS 8, Rocky 8, Alma 8)',
        'el9': 'Enterprise Linux 9 (RHEL 9, CentOS 9, Rocky 9, Alma 9)',
        'd12': 'Debian 12 (Bookworm)',
        'u22': 'Ubuntu 22.04 LTS (Jammy)',
        'u24': 'Ubuntu 24.04 LTS (Noble)'
    }
    
    for os_base in ['el8', 'el9', 'd12', 'u22', 'u24']:
        x86_packages = os_groups.get(f'{os_base}.x86_64', set())
        arm_packages = os_groups.get(f'{os_base}.aarch64', set())
        
        # Get extensions available on this OS
        all_os_packages = x86_packages | arm_packages
        available_extensions = [ext for ext in extensions if ext.pkg in all_os_packages]
        available_extensions.sort(key=lambda e: e.name)
        
        section = f'''
## {os_base.upper()}

{os_map[os_base]}

<Badge variant="blue-subtle">x86_64</Badge> <Badge variant="gray-subtle">{len(x86_packages)} Packages</Badge>

<Badge variant="orange-subtle">aarch64</Badge> <Badge variant="gray-subtle">{len(arm_packages)} Packages</Badge>

<Badge variant="green-subtle">Total</Badge> <Badge variant="gray-subtle">{len(available_extensions)} Extensions</Badge>

'''
        os_sections.append(section)

    content = f'''---
title: By Linux
description: PostgreSQL extensions availability by Linux distros
icon: Server
full: true
---

import {{ Badge }} from '@/components/ui/badge';

{''.join(os_sections)}
'''
    
    output_path = os.path.join(OUTPUT_DIR, 'linux.mdx')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Generated: {output_path}")

def gen_pg_major_list(extensions: List['Extension']):
    """Generate By PG Major unavailable extensions list (content/ext/list/pg.mdx)."""
    print("Generating PG major list...")
    
    pg_sections = []
    for pg in DEFAULT_PG:
        # Find extensions NOT available for this PG version
        unavailable_extensions = [ext for ext in extensions if str(pg) not in ext.pg_ver]
        unavailable_extensions.sort(key=lambda e: e.name)
        
        section = f'''
## PostgreSQL {pg}

Extensions **NOT available** for PostgreSQL {pg}

{generate_simple_extension_table(unavailable_extensions)}
'''
        pg_sections.append(section)
    
    content = f'''---
title: By PostgreSQL
description: PostgreSQL extensions unavailable by major version
icon: Database
full: true
---

import {{ Badge }} from '@/components/ui/badge';

{''.join(pg_sections)}
'''
    
    output_path = os.path.join(OUTPUT_DIR, 'pg.mdx')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Generated: {output_path}")

def gen_license_list(extensions: List['Extension']):
    """Generate By License list (content/ext/list/license.mdx)."""
    print("Generating license list...")
    
    # Count extensions by license and normalize names
    license_counts = Counter()
    license_extensions_map = defaultdict(list)
    
    for ext in extensions:
        if not ext.license:
            continue
        # Normalize license names to standard format
        normalized_name = get_normalized_license_name(ext.license)
        license_counts[normalized_name] += 1
        license_extensions_map[normalized_name].append(ext)
    
    # License URLs and descriptions
    license_info = {
        'PostgreSQL': {
            'url': 'https://opensource.org/licenses/postgresql',
            'description': 'Very liberal license based on the BSD license, allowing almost unlimited freedom.'
        },
        'MIT': {
            'url': 'https://opensource.org/licenses/MIT',
            'description': 'A permissive license that allows commercial use, modification, and private use.'
        },
        'ISC': {
            'url': 'https://opensource.org/licenses/ISC',
            'description': 'A permissive license similar to MIT, allowing commercial use and modification.'
        },
        'BSD 0-Clause': {
            'url': 'https://opensource.org/license/0bsd',
            'description': 'Public domain equivalent license with no restrictions on use.'
        },
        'BSD 2-Clause': {
            'url': 'https://opensource.org/license/bsd-2-clause',
            'description': 'Permissive license requiring attribution but allowing commercial use.'
        },
        'BSD 3-Clause': {
            'url': 'https://opensource.org/license/bsd-3-clause',
            'description': 'Permissive license with attribution and endorsement restriction clauses.'
        },
        'Artistic': {
            'url': 'https://opensource.org/license/artistic-2-0',
            'description': 'Copyleft license allowing modification with certain distribution requirements.'
        },
        'Apache-2.0': {
            'url': 'https://opensource.org/licenses/Apache-2.0',
            'description': 'Permissive license with patent protection and attribution requirements.'
        },
        'MPL-2.0': {
            'url': 'https://opensource.org/licenses/MPL-2.0',
            'description': 'Weak copyleft license allowing proprietary combinations with file-level copyleft.'
        },
        'GPL-2.0': {
            'url': 'https://opensource.org/licenses/GPL-2.0',
            'description': 'Strong copyleft license requiring derivative works to be open source.'
        },
        'GPL-3.0': {
            'url': 'https://opensource.org/licenses/GPL-3.0',
            'description': 'Strong copyleft license with additional patent and hardware restrictions.'
        },
        'LGPL-2.1': {
            'url': 'https://opensource.org/licenses/LGPL-2.1',
            'description': 'Weak copyleft license allowing proprietary applications to link dynamically.'
        },
        'LGPL-3.0': {
            'url': 'https://opensource.org/licenses/LGPL-3.0',
            'description': 'Weak copyleft license with additional patent and hardware provisions.'
        },
        'AGPL-3.0': {
            'url': 'https://opensource.org/licenses/AGPL-3.0',
            'description': 'Network copyleft license extending GPL to cover network-distributed software.'
        },
        'Timescale': {
            'url': 'https://www.timescale.com/legal/licenses',
            'description': 'Proprietary license with restrictions on commercial use and distribution.'
        }
    }
    
    # Generate summary table
    summary_rows = []
    for license_name, count in license_counts.most_common():
        info = license_info.get(license_name, {'url': '#'})
        summary_rows.append(f'| {format_license_badge(license_name)} | {count} | [License Text]({info["url"]}) | {info["description"]} |')
    
    summary_table = f'''| License | Count | Reference |  Description |
|:--------|:-----:|:-------:|:----------|
{chr(10).join(summary_rows)}'''
    
    # Generate license sections
    license_sections = []
    for license_name, count in license_counts.most_common():
        license_extensions = sorted(license_extensions_map[license_name], key=lambda e: e.name)
        info = license_info.get(license_name, {})
        
        # Generate anchor for the license
        anchor = license_name.lower().replace(' ', '-').replace('.', '')
        
        section = f'''
## {license_name}

{format_license_badge(license_name)} <Badge icon={{<Package />}} variant="gray-subtle">{count} Extensions</Badge>

[{license_name} License Text]({info.get("url", "#")}) : {info.get("description", "Open source license.")}

{generate_simple_extension_table(license_extensions)}
'''
        license_sections.append(section)
    
    content = f'''---
title: By License
description: PostgreSQL extensions organized by open source license
icon: Scale
full: true
---

import {{ Badge }} from '@/components/ui/badge';
import {{ Scale, Package }} from 'lucide-react';

<a href="#mit"          className="no-underline"><Badge icon={{<Scale />}} variant="blue-subtle"  >MIT</Badge></a>
<a href="#isc"          className="no-underline"><Badge icon={{<Scale />}} variant="blue-subtle"  >ISC</Badge></a>
<a href="#postgresql"   className="no-underline"><Badge icon={{<Scale />}} variant="blue-subtle"  >PostgreSQL</Badge></a>
<a href="#bsd-0-clause" className="no-underline"><Badge icon={{<Scale />}} variant="blue-subtle"  >BSD 0-Clause</Badge></a>
<a href="#bsd-2-clause" className="no-underline"><Badge icon={{<Scale />}} variant="blue-subtle"  >BSD 2-Clause</Badge></a>
<a href="#bsd-3-clause" className="no-underline"><Badge icon={{<Scale />}} variant="blue-subtle"  >BSD 3-Clause</Badge></a>
<a href="#artistic"     className="no-underline"><Badge icon={{<Scale />}} variant="green-subtle" >Artistic</Badge></a>
<a href="#apache-20"    className="no-underline"><Badge icon={{<Scale />}} variant="green-subtle" >Apache-2.0</Badge></a>
<a href="#mpl-20"       className="no-underline"><Badge icon={{<Scale />}} variant="green-subtle" >MPL-2.0</Badge></a><br />
<a href="#gpl-20"       className="no-underline"><Badge icon={{<Scale />}} variant="amber-subtle" >GPL-2.0</Badge></a>
<a href="#gpl-30"       className="no-underline"><Badge icon={{<Scale />}} variant="amber-subtle" >GPL-3.0</Badge></a>
<a href="#lgpl-21"      className="no-underline"><Badge icon={{<Scale />}} variant="amber-subtle" >LGPL-2.1</Badge></a>
<a href="#lgpl-30"      className="no-underline"><Badge icon={{<Scale />}} variant="amber-subtle" >LGPL-3.0</Badge></a>
<a href="#agpl-30"      className="no-underline"><Badge icon={{<Scale />}} variant="red-subtle"   >AGPL-3.0</Badge></a>
<a href="#timescale"    className="no-underline"><Badge icon={{<Scale />}} variant="gray-subtle"  >Timescale</Badge></a>

## Summary

{summary_table}

---------

{''.join(license_sections)}
'''
    
    output_path = os.path.join(OUTPUT_DIR, 'license.mdx')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Generated: {output_path}")

def get_normalized_license_name(license_name: str) -> str:
    """Normalize license names to standard format."""
    # Mapping of various license name variations to standard names
    normalization_map = {
        'BSD-0': 'BSD 0-Clause',
        'BSD 0-Clause': 'BSD 0-Clause',
        'BSD-2': 'BSD 2-Clause', 
        'BSD 2-Clause': 'BSD 2-Clause',
        'BSD-3': 'BSD 3-Clause',
        'BSD 3-Clause': 'BSD 3-Clause',
        'GPLv2': 'GPL-2.0',
        'GPL-2.0': 'GPL-2.0',
        'GPLv3': 'GPL-3.0',
        'GPL-3.0': 'GPL-3.0',
        'LGPLv2': 'LGPL-2.1',
        'LGPL-2.1': 'LGPL-2.1',
        'LGPLv3': 'LGPL-3.0',
        'LGPL-3.0': 'LGPL-3.0',
        'AGPLv3': 'AGPL-3.0',
        'AGPL-3.0': 'AGPL-3.0',
        'MPLv2': 'MPL-2.0',
        'MPL-2.0': 'MPL-2.0'
    }
    
    return normalization_map.get(license_name, license_name)

def gen_language_list(extensions: List['Extension']):
    """Generate By Language list (content/ext/list/lang.mdx)."""
    print("Generating language list...")
    
    # Count extensions by language
    language_counts = Counter(ext.lang for ext in extensions if ext.lang)
    
    # Language descriptions
    language_descriptions = {
        'C': 'The traditional PostgreSQL extension language',
        'C++': 'Extensions leveraging C++ features and libraries',
        'Rust': 'Extensions written in Rust with the pgrx framework',
        'Python': 'Extensions written in Python',
        'SQL': 'Pure SQL extensions and functions',
        'Java': 'Extensions running on JVM',
        'Data': 'Data-only extensions',
    }
    
    # Generate summary table
    summary_rows = []
    for lang, count in language_counts.most_common():
        desc = language_descriptions.get(lang, 'Extensions written in this language')
        summary_rows.append(f'| {format_language_badge(lang)} | {count} | {desc} |')
    
    summary_table = f'''| Language | Count | Description |
|:-------:|:-----:|:------------|
{chr(10).join(summary_rows)}'''
    
    # Generate language sections
    language_sections = []
    for lang, count in language_counts.most_common():
        lang_extensions = [ext for ext in extensions if ext.lang == lang]
        lang_extensions.sort(key=lambda e: e.name)
        
        desc = language_descriptions.get(lang, f'Extensions written in {lang}')
        
        section = f'''
## {lang}

{format_language_badge(lang)} <Badge icon={{<Package />}} variant="gray-subtle">{count} Extensions</Badge>

{desc}

{generate_simple_extension_table(lang_extensions)}
'''
        language_sections.append(section)
    
    content = f'''---
title: By Language
description: PostgreSQL extensions organized by implementation language
icon: FileCode2
full: true
---

import {{ Badge }} from '@/components/ui/badge';
import {{ FileCode2, Package }} from 'lucide-react';

<a href="/ext/list/lang#c"><Badge      icon={{<FileCode2 />}} variant="blue-subtle">C</Badge></a>
<a href="/ext/list/lang#c-1"><Badge    icon={{<FileCode2 />}} variant="purple-subtle">C++</Badge></a>
<a href="/ext/list/lang#rust"><Badge   icon={{<FileCode2 />}} variant="amber-subtle">Rust</Badge></a>
<a href="/ext/list/lang#java"><Badge   icon={{<FileCode2 />}} variant="pink-subtle">Java</Badge></a>
<a href="/ext/list/lang#python"><Badge icon={{<FileCode2 />}} variant="blue-subtle">Python</Badge></a>
<a href="/ext/list/lang#sql"><Badge    icon={{<FileCode2 />}} variant="green-subtle">SQL</Badge></a>
<a href="/ext/list/lang#data"><Badge   icon={{<FileCode2 />}} variant="teal-subtle">Data</Badge></a>

## Summary

{summary_table}

{''.join(language_sections)}
'''
    
    output_path = os.path.join(OUTPUT_DIR, 'lang.mdx')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Generated: {output_path}")

def gen_inventory_index(extensions: List['Extension']):
    """Generate overall inventory index (content/ext/list/index.mdx)."""
    print("Generating inventory index...")
    
    # Generate statistics
    total_extensions = len(extensions)
    contrib_count = len([ext for ext in extensions if ext.contrib])
    third_party_count = total_extensions - contrib_count
    
    # Count by categories
    category_counts = defaultdict(int)
    for ext in extensions:
        category_counts[ext.category] += 1
    
    # Count by licenses
    license_counts = Counter(ext.license for ext in extensions if ext.license)
    
    # Count by languages
    language_counts = Counter(ext.lang for ext in extensions if ext.lang)
    
    # Generate statistics section
    stats_content = f'''
## Statistics

<Badge variant="blue-subtle">Total</Badge> <Badge variant="gray-subtle">{total_extensions} Extensions</Badge>

<Badge variant="green-subtle">Contrib</Badge> <Badge variant="gray-subtle">{contrib_count} Extensions</Badge>

<Badge variant="purple-subtle">Third-party</Badge> <Badge variant="gray-subtle">{third_party_count} Extensions</Badge>

<Badge variant="amber-subtle">Categories</Badge> <Badge variant="gray-subtle">{len(category_counts)} Categories</Badge>

<Badge variant="teal-subtle">Licenses</Badge> <Badge variant="gray-subtle">{len(license_counts)} Licenses</Badge>

<Badge variant="pink-subtle">Languages</Badge> <Badge variant="gray-subtle">{len(language_counts)} Languages</Badge>
'''
    
    # Generate extensions by category
    extensions_content = []
    for category in CATEGORY_META.keys():
        cat_extensions = [ext for ext in extensions if ext.category == category]
        if not cat_extensions:
            continue
            
        cat_extensions.sort(key=lambda e: e.name)
        extension_badges = []
        for ext in cat_extensions:
            extension_badges.append(f'[`{ext.name}`](/ext/{ext.name})')
        
        extensions_row = f'''| {format_category_badge(category)} | {' '.join(extension_badges)} |'''
        extensions_content.append(extensions_row)
    
    extensions_table = f'''| Category | Extensions |
|:---------|:-----------|
{chr(10).join(extensions_content)}'''
    
    content = f'''---
title: Inventory
description: Available PostgreSQL Extensions
icon: ClipboardList
full: true
---

import {{ Badge }} from '@/components/ui/badge';
import {{ Clock, Globe, Brain, Search, ChartNoAxesCombined, Sparkles, BookA, Boxes, Wrench, Variable, Landmark, Activity, Shield, FileInput, Shell, Truck }} from 'lucide-react';

{stats_content}

## Categories

{extensions_table}
'''
    
    output_path = os.path.join(OUTPUT_DIR, 'index.mdx')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Generated: {output_path}")

def main():
    # Load extensions data
    extensions = load_extensions()
    
    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Generate all list pages
    gen_category_list(extensions)
    gen_linux_distro_list(extensions)
    gen_pg_major_list(extensions)
    gen_license_list(extensions)
    gen_language_list(extensions)
    gen_inventory_index(extensions)
    
    print("List generation complete!")

if __name__ == "__main__":
    main()