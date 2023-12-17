from marshmallow import Schema, fields, EXCLUDE


class Task:
    def __init__(self, id, name, project_id, assignee_ids, assignee_id, user_group_ids, estimate, status, budget_estimate, duration, billable, hourly_rate, cost_rate):
        self.id = id
        self.name = name
        self.project_id = project_id
        self.assignee_ids = assignee_ids
        self.assignee_id = assignee_id
        self.user_group_ids = user_group_ids
        self.estimate = estimate
        self.status = status
        self.budget_estimate = budget_estimate
        self.duration = duration
        self.billable = billable
        self.hourly_rate = hourly_rate
        self.cost_rate = cost_rate

    def __str__(self):
        return f"Task(ID: {self.id}, Name: {self.name}, Project ID: {self.project_id}, Status: {self.status}, Estimate: {self.estimate}, Assignee IDs: {self.assignee_ids}, Assignee ID: {self.assignee_id}, User Group IDs: {self.user_group_ids}, Budget Estimate: {self.budget_estimate}, Duration: {self.duration}, Billable: {self.billable}, Hourly Rate: {self.hourly_rate}, Cost Rate: {self.cost_rate})"


class TaskSchema(Schema):
    id = fields.Str()
    name = fields.Str()
    project_id = fields.Str(data_key='projectId')
    assignee_ids = fields.List(fields.Str(), data_key='assigneeIds')
    assignee_id = fields.Str(data_key='assigneeId', allow_none=True)
    user_group_ids = fields.List(fields.Str(), data_key='userGroupIds')
    estimate = fields.Str()
    status = fields.Str()
    budget_estimate = fields.Float(data_key='budgetEstimate')
    duration = fields.Str()
    billable = fields.Boolean()
    hourly_rate = fields.Float(data_key='hourlyRate', allow_none=True)
    cost_rate = fields.Float(data_key='costRate', allow_none=True)

    class Meta:
        unknown = EXCLUDE  # Exclude fields not specified in the schema
