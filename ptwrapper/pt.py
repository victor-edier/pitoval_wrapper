import requests
import json
import unicodedata


class PT(object):
  def __init__(self, project_id=None, token=None):
    self.project_id = project_id
    self.token = token
  
  def set_token(self, token=None):
    self.token = token

  def get_request_json(self, url_part):
    project_id = self.project_id
    url = 'https://www.pivotaltracker.com/services/v5/projects/'+project_id+'/'+url_part
    try:
      r = requests.get(url,headers={'X-TrackerToken': self.token})
      content = r.content
      result = json.loads(content)
    except Exception as e:
      result = []
    return result

  def strip_string(self, raw_string):
    if isinstance(raw_string, str):
      raw_string = unicodedata.normalize('NFKD', raw_string).encode('ascii', 'ignore')
    if not isinstance(raw_string, str):
      raw_string = str(raw_string, 'utf-8')
    return raw_string.strip()

  def get_story_data_by_raw(self, raw_story):
    x = {}
    x['id']            = str(raw_story['id'])
    x['url']           = self.strip_string(raw_story['url'])
    x['name']          = self.strip_string(raw_story['name'])
    x['story_type']    = self.strip_string(raw_story['story_type'])
    x['current_state'] = self.strip_string(raw_story['current_state'])
    if x['current_state'] == 'accepted':
      x['title'] = '[' + x['id'] + '] <Accepted> ' + x['name']
    else:
      x['title'] = '[' + x['id'] + '] ' + x['name']
    branches = {}
    if raw_story['branches']:
      for raw_branch in raw_story['branches']:
        branch_name = self.strip_string(raw_branch['name'])
        branch_repo = self.strip_string(raw_branch['repo'])
        b_list = branches[branch_repo] if branch_repo in branches else []
        b_list.append(branch_name)
        b_list = list(set(b_list))
        branches[branch_repo] = b_list

    x['branches'] = branches
    return x

  def get_releases(self):
    raw_relases = self.get_request_json('releases/?with_state=unstarted')
    releases = []
    for raw_release in raw_relases:
      x = {}
      x['id']   = int(raw_release['id'])
      x['name'] = self.strip_string(raw_release['name'])
      releases.append(x.copy())
    return releases

  def get_release_id(self, release_name):
    releases = self.get_releases()
    release_id = ''
    if release_name:
      for release in releases:
        if release_name == release['name']:
          release_id = release['id']
          break
    return release_id
  
  def get_stories_by_release_name(self, release_name, accepted=False):
    release_id = self.get_release_id(release_name)
    return self.get_stories_by_release(release_id, accepted)

  def get_stories_by_release(self, release_id, accepted=False):
    release_id = str(release_id)
    raw_stories = self.get_request_json('releases/'+release_id+'/stories/?fields=current_state,name,story_type,url,branches')
    stories = []
    for raw_story in raw_stories:
      x = self.get_story_data_by_raw(raw_story)
      if x['current_state'] == 'unscheduled': continue
      if x['current_state'] == 'unstarted':   continue
      if x['current_state'] == 'accepted':
        if not accepted:
          continue
      stories.append(x.copy())
    return stories