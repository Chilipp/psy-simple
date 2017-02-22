#!/bin/bash
set -e # Exit with nonzero exit code if anything fails
set -x

SRC_DIR=$1
shift
TARGET_BRANCH=$1
shift
WHAT=$@

SHA=`git rev-parse --verify HEAD`

cd $SRC_DIR

REPO_NAME=`git config remote.origin.url`
REPO_NAME=${REPO_NAME#https://}

# Now let's go have some fun with the cloned repo
git config user.name "Travis"
git config user.email "$COMMIT_AUTHOR_EMAIL"

git add -N $WHAT

# If there are no changes to the compiled out (e.g. this is a README update) then just bail.
if [ -z `git diff --exit-code` ]; then
    echo "No changes to the output on this push; exiting."
    exit 0
fi

# Commit the "changes", i.e. the new version.
git commit -am "Deploy from Travis job $TRAVIS_JOB_NUMBER: Commit ${SHA} [skip ci]"

# Now that we're all set up, we can push.
# Since we push in parallel, and the remote repository might be locked, we give
# it 10 tries

git checkout $TARGET_BRANCH

set +ex

for COUNTER in {1..10} ; do
    echo Try No. ${COUNTER}: git pull && git rebase TRAVIS_DEPLOY && git push "https://<secure>@${REPO_NAME}" $TARGET_BRANCH
    git pull "https://${GH_REPO_TOKEN}@${REPO_NAME}" $TARGET_BRANCH
    git rebase TRAVIS_DEPLOY
    git push "https://${GH_REPO_TOKEN}@${REPO_NAME}" $TARGET_BRANCH  &> log.txt
    if [[ $? != 0 ]]; then  # push failed, wait 10 seconds and try again
        # print the log
        sed -e "s/${GH_REPO_TOKEN}/<secure>/g" log.txt
        if [[ $COUNTER == 10 ]]; then
            exit 1
        fi
        echo "Retrying in 10 seconds..."
        sleep 10
    else  # push successed, exit loop
        break
    fi
done
