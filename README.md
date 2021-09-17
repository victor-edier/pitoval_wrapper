# ptwrapper: Pivotal Tracker Wrapper
Yet Another Wrapper for Pivotal Tracker written in Python, ptwrapper is a simple wrapper to get stories from Pivotal Tracker

## Features
- Get stories by release id or release name

## Usage
This is an example to get the branches associated with stories in a release
```
from ptwrapper import PT
project_id = 'XXXXXX'
user_token = 'XXXXXXXXXXXXXXXXXXXXXXXXXX'
release_name = 'XXXX'
pivotal = PT(project_id, user_token)
stories = pivotal.get_stories_by_release_name(release_name)
for story in stories:
  print(story['title'])
  for branch_repo in story['branches']:
    branches = story['branches'][branch_repo]
    print('    Repository:', branch_repo)
    for branch in branches:
      print('        Branch:', branch)
```

## Requirements
- requests

## Installation
Just download this repository and execute
```
pip3 install -e .
```
