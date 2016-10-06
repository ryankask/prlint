.. image:: https://circleci.com/gh/jamescooke/prlint.svg?style=shield
    :target: https://circleci.com/gh/jamescooke/prlint

About
=====

PRLint is a linter for pull requests. Primarily it integrates with GitHub and
works with the GitHub style of Pull Request.

The majority of testing services test the ``HEAD`` commit of a Pull Request.
This is fine when a team only care about the final patch about to be applied or
where every successful pull request is squashed to a single commit. However,
some teams maintain git history and there are some conditions where the team
may care about each commit in a pull request.

Fixup commits
-------------

Take, for example, ``--fixup`` commits. In `Pull Request #1 </pull/1>`_ there
is a fixup commit waiting to be squashed - it's highlighted here in red:

.. image:: assets/fixup_commit.png

Although the diff of the pull request is valid, we want to block the merge of
the pull request until the fixup commit is autosquashed.

PRLint tests every commit in a pull request and fails if any commit doesn't
pass the rules set for the repository.

    PRLint was originally called "nofixup" because it was built to catch fixup
    commits and fail the pull request if any where in the commits of the PR.
    You can read more about `fixup commits and autosquashing in this thoughtbot
    article <https://robots.thoughtbot.com/autosquashing-git-commits>`_.

Values
------

* Open and accessible always: The project is open-source, you can take it and
  run your own instance.

* Generic and flexible: Although PRLint is written in Python, it can be used
  with any repository written in any languages. It aims to support as many
  workflows as possible.


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
