from invoke import task


@task
def start(ctx):
    ctx.run("python src/main.py", pty=True)


@task
def test(ctx):
    ctx.run("pytest src")


# @task
# def lint(ctx):
#     ctx.run("pylint src", pty=True)


# @task
# def format(ctx):  # pylint: disable=redefined-builtin
#     ctx.run("autopep8 --in-place --recursive src", pty=True)


@task
def coverage(ctx):
    ctx.run("coverage run --branch -m pytest src")


@task(coverage)
def coverage_report(ctx):
    ctx.run("coverage html")