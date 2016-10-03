# Webhook: Receive Pull Request event

See [Receive GitHub webhook](post.md) for common behaviour.

According [to the docs](https://developer.github.com/webhooks/#events), pull
requests are triggered...

> any time a Pull Request is assigned, unassigned, labeled, unlabeled, opened,
> edited, closed, reopened, or synchronized (updated due to a new push in the
> branch that the pull request is tracking).

In addition to


* Assert that the incoming pull request is from a repository that is registered
    with the service.

The main functions of this endpoint are to:


* Create a record for the pull request and queue it for testing.

* Queue a response to the GitHub Status API that the `HEAD` commit of the pull
    request is `pending`.

* Respond with a `200 OK` status code to GitHub.


**URL** : `/api/github/`

**Method** : `POST`

**Auth required** : NO

**Permissions required** : None

**Header constraints**

* `X-GitHub-Event: pull_request`


**Condition** : If everything is OK and an Account didn't exist for this User.

**Code** : `200 OK`

**Content example**
