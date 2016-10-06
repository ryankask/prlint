A linter for Pull Requests
==========================

.. image:: https://circleci.com/gh/jamescooke/prlint.svg?style=shield
    :target: https://circleci.com/gh/jamescooke/prlint

PRLint lints each Pull Request's commits against a set of rules, failing Pull
Requests that contain commits that do not meet the required standards. In this
way it helps developers by improving the quality of git history entering a
repository.

Not just ``HEAD``
-----------------

The majority of testing services test just the ``HEAD`` commit of a Pull
Request. This is fine when a team only care about the final patch about to be
applied or where every successful Pull Request is squashed to a single commit.
However, some teams maintain git history and there are some conditions where
the team may care about each commit in a Pull Request.

Fixup commits
-------------

Take, for example, ``--fixup`` commits. In `Pull Request #1
<https://github.com/jamescooke/prlint/pull/1>`_ there is a fixup commit waiting
to be squashed - it's highlighted here in red:

.. image:: assets/fixup_commit.png

Although the diff of the Pull Request is valid, we want to block the merge of
the Pull Request until the fixup commit is autosquashed. Otherwise the fixup
commit will enter our master branch and pollute the history.

PRLint tests every commit in a Pull Request and fails if any commit doesn't
pass the rules set for the repository.

    TODO: Add failing status image and resolution.

Further info
------------

PRLint was originally called "nofixup" because it was built to catch fixup
commits and set the ``HEAD`` commit of the Pull Request to failing if any were
found.

You can read more about `fixup commits and autosquashing in this thoughtbot
article <https://robots.thoughtbot.com/autosquashing-git-commits>`_.

Values
------

* Open and accessible always: The `project is open-source </LICENSE>`_, you can
  take it and run your own instance.

* Generic and flexible: Although PRLint is written in Python, it can be used
  with any repository written in any languages. It aims to support as many
  workflows as possible.

* Multiple integrations: Primarily PRLint integrates with GitHub and works with
  the GitHub style of Pull Request. PRLint will integrate with as many services
  as possible.


Install
=======

Clone this repository.

Create a virtualenv containing Python3::

    make venv

Activate and install requirements::

    . venv/bin/activate
    make install

Testing
=======

While in virtualenv, add the testing requirements::

    make install-test

Run tests with Django's test runner which is configured to use Nose::

    make test

Check linting with ``flake8``::

    make lint
