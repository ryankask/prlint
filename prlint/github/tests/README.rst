Payload Factories
=================

Notes about the structure of the factories used to generate GitHub payloads.

Map
---

There are two main factories which are used to create requests that look like
valid event payloads from GitHub: ``PingEventFactory`` and
``PullRequestEventFactory`` (TODO).

Both of these factories use ``PayloadRequestFactory`` to generate a request,
set the ``X-GitHub-Event`` header and populates the body with the appropriate
event's payload.

Those events each have their own chain of factories that are used to generate
different parts of the payloads. The calling tree is as follows:

Ping
....

* ``PingEventFactory``

  Builds the data with:

  - ``PingPayloadFactory`` calls two sub-factories:

    * ``RepositoryPayloadFactory``

    * ``HookPayloadFactory``

  Stuffs the data in the request envelope with:

  - ``PayloadRequestFactory(header__event='ping', ...)``

Pull Request
............

* ``PullRequestEventFactory``

  - ``PayloadRequestFactory(header__event='pull_request', ...)``

    * TODO

Data
----

It is possible to create a Request that would never be sent by GitHub in a
number of ways. These conditions are not currently checked by the factories to
ensure that only valid Requests are constructed, although the goal is that the
factories would only generate "good" requests in the future.

Some examples:

- Pass a hook configuration which contains a limited number of events and
  then issue a non-ping event that is not in that list. For example::

      PayloadRequestFactory(header__event='pull_request', hook_events=['commit'])

- Pass a ``repository_id`` that is negative or stringy.
