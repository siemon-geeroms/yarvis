# yarvis
custom integration that extents the default speech to text engine of home assistant with regex capabilities.
## Usage/Examples

After the integration is installed succesfully it can be configuered to trigger [intent scripts](https://www.home-assistant.io/integrations/intent_script).

The sentences will be parsed as an regex and if a match is found the intent will be triggered. when named groups are used these will be passed to the intent script as variables.

When no matches are found the default home assistant intent parser is being triggered. 

### config
```yaml
playMedia:
  sentences:
    - play (?P<movie>.*?) on tv
addTask:
  sentences:
    - add (?P<task>.*?) to (?P<project>.*?$)

```
### intent scripts
```yaml
intent_script:
  playMedia:
    speech:
      text: "playing {{movie}} on tv"
    action:
      service: script.playMovie
      data:
        movie: "\{\{movie\}}"
  addTask:
    speech:
      text: "{{task}} added to {{project}}"
    action:
      service: todoist.new_task
      data:
        "content": "{{task}}"
        "project": "{{project}}"
```
