from marshmallow import Schema, fields, EXCLUDE


class Project:
    def __init__(self, id, name, hourly_rate, client_id, workspace_id, billable, memberships, color, estimate, archived,
                 duration, client_name, note, cost_rate, time_estimate, budget_estimate, template, public):
        self.id = id
        self.name = name
        self.hourly_rate = hourly_rate
        self.client_id = client_id
        self.workspace_id = workspace_id
        self.billable = billable
        self.memberships = memberships
        self.color = color
        self.estimate = estimate
        self.archived = archived
        self.duration = duration
        self.client_name = client_name
        self.note = note
        self.cost_rate = cost_rate
        self.time_estimate = time_estimate
        self.budget_estimate = budget_estimate
        self.template = template
        self.public = public

    def __str__(self):
        return (f"Project(ID: {self.id}, Name: {self.name}, Hourly Rate: {self.hourly_rate}, "
                f"Client ID: {self.client_id}, Workspace ID: {self.workspace_id}, Billable: {self.billable}, "
                f"Memberships: {self.memberships}, Color: {self.color}, Estimate: {self.estimate}, "
                f"Archived: {self.archived}, Duration: {self.duration}, Client Name: {self.client_name}, "
                f"Note: {self.note}, Cost Rate: {self.cost_rate}, Time Estimate: {self.time_estimate}, "
                f"Budget Estimate: {self.budget_estimate}, Template: {self.template}, Public: {self.public})")


class HourlyRateSchema(Schema):
    amount = fields.Float()
    currency = fields.Str()


class MembershipSchema(Schema):
    userId = fields.Str()
    hourlyRate = fields.Float(allow_none=True)
    costRate = fields.Float(allow_none=True)
    targetId = fields.Str()
    membershipType = fields.Str()
    membershipStatus = fields.Str()


class EstimateSchema(Schema):
    estimate = fields.Str()
    type = fields.Str()


class TimeEstimateSchema(Schema):
    estimate = fields.Str()
    type = fields.Str()
    resetOption = fields.Str(allow_none=True)
    active = fields.Boolean()
    includeNonBillable = fields.Boolean()


class ProjectSchema(Schema):
    id = fields.Str()
    name = fields.Str()
    hourly_rate = fields.Nested(HourlyRateSchema(), data_key='hourlyRate')
    client_id = fields.Str(data_key='clientId')
    workspace_id = fields.Str(data_key='workspaceId')
    billable = fields.Boolean()
    memberships = fields.List(fields.Nested(MembershipSchema()))
    color = fields.Str()
    estimate = fields.Nested(EstimateSchema())
    archived = fields.Boolean()
    duration = fields.Str()
    client_name = fields.Str(data_key='clientName')
    note = fields.Str()
    cost_rate = fields.Float(allow_none=True, data_key='costRate')
    time_estimate = fields.Nested(TimeEstimateSchema(), data_key='timeEstimate')
    budget_estimate = fields.Float(allow_none=True, data_key='budgetEstimate')
    template = fields.Boolean()
    public = fields.Boolean()

    class Meta:
        unknown = EXCLUDE
