
--------

## Usage

The actual PDF parsing is done by [poppler](https://poppler.freedesktop.org).

This allows you to work with PDFs in an ACID-compliant way.
The usual alternative relies on external scripts or services which can easily
make your data ingestion pipeline brittle and leave your raw data out-of-sync.

- [Full Text Search on PDFs With Postgres](https://tselai.com/full-text-search-pdf-postgres)
- [pgpdf: pdf type for Postgres](https://tselai.com/pgpdf-pdf-type-postgres)

Download some PDFs.

```sh
wget https://wiki.postgresql.org/images/e/ea/PostgreSQL_Introduction.pdf -O /tmp/pgintro.pdf
wget https://pdfobject.com/pdf/sample.pdf -O /tmp/sample.pdf
```

You can create a `pdf` type, by casting either a `text` filepath or `bytea` column.

```sql
CREATE EXTENSION pgpdf;
SELECT '/tmp/pgintro.pdf'::pdf;
```

```sql
                                       pdf                                        
----------------------------------------------------------------------------------
 PostgreSQL Introduction                                                         +
 Digoal.Zhou                                                                     +
 7/20/2011Catalog                                                                +
  PostgreSQL Origin 
```

If you don’t have the PDF file in your filesystem, but have already stored its content in a `bytea` column, you can just cast it to `pdf`.

```sql
SELECT pg_read_binary_file('/tmp/pgintro.pdf')::bytea::pdf;
```

--------

## Examples

Create a table with a `pdf` column:

```sql
CREATE TABLE pdfs(name text primary key, doc pdf);

INSERT INTO pdfs VALUES ('pgintro', '/tmp/pgintro.pdf');
INSERT INTO pdfs VALUES ('pgintro', '/tmp/sample.pdf');
```

Parsing and validation should happen automatically.
The files will be read from the disk only once!

> [!NOTE]
> The filepath should be accessible by the `postgres` process / user!
> That's different than the user running psql.
> If you don't understand what this means, as your DBA!

### String Functions and Operators

Standard Postgres [String Functions and Operators](https://www.postgresql.org/docs/17/functions-string.html)
should work as usual:

```sql
SELECT 'Below is the PDF we received ' || '/tmp/pgintro.pdf'::pdf;
```

```sql
SELECT upper('/tmp/pgintro.pdf'::pdf::text);
```

```sql
SELECT name
FROM pdfs
WHERE doc::text LIKE '%Postgres%';
```

### Full-Text Search (FTS)

You can also perform full-text search (FTS), since you can work on a `pdf` file like normal text.

```sql
SELECT '/tmp/pgintro.pdf'::pdf::text @@ to_tsquery('postgres');
```

```sql
 ?column? 
----------
 t
(1 row)
```

```sql
SELECT '/tmp/pgintro.pdf'::pdf::text @@ to_tsquery('oracle');
```

```sql
 ?column? 
----------
 f
(1 row)
```

### Document similarity with `pg_trgm`

You can use [pg_trgm](https://postgresql.org/docs/17/interactive/pgtrgm.html)
to get the similarity between two documents:

```sql
CREATE EXTENSION pg_trgm;

SELECT similarity('/tmp/pgintro.pdf'::pdf::text, '/tmp/sample.pdf'::pdf::text);
```

### Metadata

The following functions are available:

- `pdf_title(pdf) → text`
- `pdf_author(pdf) → text`
- `pdf_num_pages(pdf) → integer`

  Total number of pages in the document
- `pdf_page(pdf, integer) → text`

  Get the i-th page as text
- `pdf_creator(pdf) → text`
- `pdf_keywords(pdf) → text`
- `pdf_metadata(pdf) → text`
- `pdf_version(pdf) → text`
- `pdf_subject(pdf) → text`
- `pdf_creation(pdf) → timestamp`
- `pdf_modification(pdf) → timestamp`

```sql
SELECT pdf_title('/tmp/pgintro.pdf');
```

```sql
        pdf_title        
-------------------------
 PostgreSQL Introduction
(1 row)
```

```sql
SELECT pdf_author('/tmp/pgintro.pdf');
```

```sql
 pdf_author 
------------
 周正中
(1 row)
```

Getting a subset of pages

```sql
SELECT pdf_num_pages('/tmp/pgintro.pdf');
```

```sql
 pdf_num_pages 
---------------
            24
(1 row)
```

```sql
SELECT pdf_page('/tmp/pgintro.pdf', 1);
```

```sql
           pdf_page           
------------------------------
 Catalog                     +
  PostgreSQL Origin         +
  Layout                    +
  Features                  +
  Enterprise Class Attribute+
  Case
(1 row)
```

```sql
SELECT pdf_subject('/tmp/pgintro.pdf');
```

```sql
 pdf_subject 
-------------
 
(1 row)
```

```sql
SELECT pdf_creation('/tmp/pgintro.pdf');
```

```sql
       pdf_creation       
--------------------------
 Wed Jul 20 11:13:37 2011
(1 row)
```

```sql
SELECT pdf_modification('/tmp/pgintro.pdf');
```

```sql
     pdf_modification     
--------------------------
 Wed Jul 20 11:13:37 2011
(1 row)
```

```sql
SELECT pdf_creator('/tmp/pgintro.pdf');
```

```sql
            pdf_creator             
------------------------------------
 Microsoft® Office PowerPoint® 2007
(1 row)
```

```sql
SELECT pdf_metadata('/tmp/pgintro.pdf');
```

```sql
 pdf_metadata 
--------------
 
(1 row)
```

```sql
SELECT pdf_version('/tmp/pgintro.pdf');
```

```sql
 pdf_version 
-------------
 PDF-1.5
(1 row)
```

## Installation

Install [poppler](https://poppler.freedesktop.org) dependencies

**Linux**
```
sudo apt install -y libpoppler-glib-dev pkg-config
```

**Homebrew/MacOS**

```
brew install poppler pkgconf
```

```
cd /tmp
git clone https://github.com/Florents-Tselai/pgpdf.git
cd pgpdf
make
make install # may need sudo
```

After the installation, in a session:

```sql
CREATE EXTENSION pgpdf;
```

### Docker

Get the [Docker image](https://hub.docker.com/r/florents/pgpdf) with:

```sh
docker pull florents/pgpdf:pg17
```

This adds pgpdf to the [Postgres image](https://hub.docker.com/_/postgres) (replace `17` with your Postgres server version, and run it the same way).

Run the image in a container.

```sh
docker run --name pgpdf -p 5432:5432 -e POSTGRES_PASSWORD=pass florents/pgpdf:pg17
```

Through another terminal, connect to the running server (container).

```sh
PGPASSWORD=pass psql -h localhost -p 5432 -U postgres
```

> [!WARNING]
> Reading arbitrary binary data (PDF) into your database can pose security risks.
> Only use this for files you trust.
