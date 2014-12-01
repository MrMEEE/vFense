class JobCollections():
    Jobs = 'jobs'
    AdministrativeJobs = 'administrative_jobs'


class JobKeys():
    Id = 'id'
    Name = 'name'
    Kwargs = 'kwargs'
    Args = 'Args'
    Runs = 'runs'
    Operation = 'operation'
    ViewName = 'view_name'
    StartDate = 'start_date'
    EndDate = 'end_date'
    TimeZone = 'time_zone'
    NextRunTime = 'next_run_time'
    Trigger = 'trigger'
    JobState = 'job_state'
    CreatedTime = 'created_time'

class JobKwargKeys():
    Agents = 'agents'
    AllAgents = 'all_agents'
    Tags = 'tags'
    AllTags = 'all_tags'

class JobIndexes():
    NextRunTime = 'next_run_time'
    ViewName = 'view_name'
