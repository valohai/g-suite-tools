G Suite Tools
=============

A growing collection tools for managing a G Suite organization.

Before you begin
----------------

* Install the requirements into a Python 3.6+ virtualenv. (`pip install -r requirements.txt`)
* Set up an OAuth application for Google APIs. 
  Follow the instructions on [this page](https://developers.google.com/admin-sdk/directory/v1/guides/authorizing.html)
  for "installed software" authentication and once you have a `client_secret.json` file, plop it in the
  working directory here.

Retrieve all groups and their members
-------------------------------------

```
python -m gst.get_group_info --domain=mydomain.com --write-json=groups.json
```

To convert `groups.json` into a mapping of group-email -> member-emails, using Jq:

```
jq '.[]|[{"key":.email,"value":[._members[].email]}]|from_entries' groups.json
```

To convert `groups.json` into human-readable Markdown:

```
python -m gst.format_group_info --json=groups.json --write-markdown=-
```
