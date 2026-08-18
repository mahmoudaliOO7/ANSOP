"""Initial database schema.

Revision ID: 001
Revises: None
Create Date: 2025-08-18 13:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import uuid

revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create initial database schema."""
    # Create ENUM types
    sa.event.listen(
        sa.create_engine("postgresql://").dialect,
        "connect",
        lambda dbapi_conn, connection_record: None,
    )
    
    op.execute("CREATE TYPE role_type AS ENUM ('ADMIN', 'SOC_ANALYST', 'APPROVER', 'VIEWER')")
    op.execute("CREATE TYPE severity_type AS ENUM ('CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFO')")
    op.execute("CREATE TYPE detection_status_type AS ENUM ('NEW', 'ACKNOWLEDGED', 'RESOLVED', 'CLOSED')")
    op.execute("CREATE TYPE incident_status_type AS ENUM ('NEW', 'TRIAGED', 'INVESTIGATING', 'CONTAINMENT', 'RESOLVED', 'CLOSED')")
    op.execute("CREATE TYPE approval_status_type AS ENUM ('PENDING_APPROVAL', 'APPROVED', 'REJECTED', 'EXPIRED', 'EXECUTING', 'SUCCESS', 'FAILED')")
    op.execute("CREATE TYPE response_status_type AS ENUM ('PENDING', 'EXECUTING', 'SUCCESS', 'FAILED', 'ROLLED_BACK')")
    op.execute("CREATE TYPE device_type_enum AS ENUM ('FIREWALL', 'ROUTER', 'IDS', 'IDS_IPS', 'SWITCH', 'PROXY', 'SIMULATOR')")
    op.execute("CREATE TYPE audit_action_type AS ENUM ('LOGIN', 'LOGOUT', 'CREATE', 'UPDATE', 'DELETE', 'APPROVE', 'REJECT', 'EXECUTE', 'ENRICH', 'RISK_ASSESS')")

    # Users table
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.text('gen_random_uuid()'), primary_key=True),
        sa.Column('username', sa.String(255), nullable=False, unique=True),
        sa.Column('email', sa.String(255), nullable=False, unique=True),
        sa.Column('full_name', sa.String(255), nullable=True),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column('is_superuser', sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column('last_login', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
    )
    op.create_index('ix_users_username', 'users', ['username'])
    op.create_index('ix_users_email', 'users', ['email'])
    op.create_index('ix_users_created_at', 'users', ['created_at'])

    # Roles table
    op.create_table(
        'roles',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.text('gen_random_uuid()'), primary_key=True),
        sa.Column('name', sa.String(255), nullable=False, unique=True),
        sa.Column('description', sa.String(1000), nullable=True),
        sa.Column('role_type', sa.Enum('ADMIN', 'SOC_ANALYST', 'APPROVER', 'VIEWER', name='role_type'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
    )
    op.create_index('ix_roles_name', 'roles', ['name'])

    # Permissions table
    op.create_table(
        'permissions',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.text('gen_random_uuid()'), primary_key=True),
        sa.Column('name', sa.String(255), nullable=False, unique=True),
        sa.Column('description', sa.String(1000), nullable=True),
        sa.Column('resource', sa.String(255), nullable=False),
        sa.Column('action', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
    )
    op.create_index('ix_permissions_resource_action', 'permissions', ['resource', 'action'])

    # User-Role association
    op.create_table(
        'user_roles',
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('role_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('assigned_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('user_id', 'role_id'),
    )

    # Role-Permission association
    op.create_table(
        'role_permissions',
        sa.Column('role_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('permission_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('assigned_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['permission_id'], ['permissions.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('role_id', 'permission_id'),
    )

    # Detections table
    op.create_table(
        'detections',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.text('gen_random_uuid()'), primary_key=True),
        sa.Column('source', sa.String(255), nullable=False),
        sa.Column('timestamp', sa.DateTime(timezone=True), nullable=False),
        sa.Column('source_ip', sa.String(45), nullable=False),
        sa.Column('destination_ip', sa.String(45), nullable=False),
        sa.Column('source_port', sa.Integer(), nullable=True),
        sa.Column('destination_port', sa.Integer(), nullable=True),
        sa.Column('protocol', sa.String(20), nullable=False),
        sa.Column('event_type', sa.String(255), nullable=False),
        sa.Column('signature', sa.String(1000), nullable=True),
        sa.Column('severity', sa.Enum('CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFO', name='severity_type'), nullable=False),
        sa.Column('raw_event', sa.Text(), nullable=True),
        sa.Column('metadata', sa.JSON(), nullable=True),
        sa.Column('status', sa.Enum('NEW', 'ACKNOWLEDGED', 'RESOLVED', 'CLOSED', name='detection_status_type'), nullable=False, server_default='NEW'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
    )
    op.create_index('ix_detections_source_ip', 'detections', ['source_ip'])
    op.create_index('ix_detections_destination_ip', 'detections', ['destination_ip'])
    op.create_index('ix_detections_timestamp', 'detections', ['timestamp'])
    op.create_index('ix_detections_severity', 'detections', ['severity'])
    op.create_index('ix_detections_status', 'detections', ['status'])
    op.create_index('ix_detections_source', 'detections', ['source'])

    # Enrichment results table
    op.create_table(
        'enrichment_results',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.text('gen_random_uuid()'), primary_key=True),
        sa.Column('detection_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('provider', sa.String(255), nullable=False),
        sa.Column('ip_reputation_score', sa.Integer(), nullable=True),
        sa.Column('domain_reputation_score', sa.Integer(), nullable=True),
        sa.Column('threat_intelligence_data', sa.JSON(), nullable=True),
        sa.Column('geolocation', sa.JSON(), nullable=True),
        sa.Column('asset_info', sa.JSON(), nullable=True),
        sa.Column('enrichment_data', sa.JSON(), nullable=False),
        sa.Column('confidence', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['detection_id'], ['detections.id'], ondelete='CASCADE'),
    )
    op.create_index('ix_enrichment_results_detection_id', 'enrichment_results', ['detection_id'])

    # Risk assessments table
    op.create_table(
        'risk_assessments',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.text('gen_random_uuid()'), primary_key=True),
        sa.Column('detection_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('risk_score', sa.Float(), nullable=False),
        sa.Column('severity', sa.Enum('CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFO', name='severity_type'), nullable=False),
        sa.Column('confidence', sa.Float(), nullable=False),
        sa.Column('risk_factors', sa.JSON(), nullable=False),
        sa.Column('explanation', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['detection_id'], ['detections.id'], ondelete='CASCADE'),
    )
    op.create_index('ix_risk_assessments_detection_id', 'risk_assessments', ['detection_id'])
    op.create_index('ix_risk_assessments_risk_score', 'risk_assessments', ['risk_score'])

    # Rules table
    op.create_table(
        'rules',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.text('gen_random_uuid()'), primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('enabled', sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column('priority', sa.Integer(), nullable=False, server_default='100'),
        sa.Column('conditions', sa.JSON(), nullable=False),
        sa.Column('actions', sa.JSON(), nullable=False),
        sa.Column('version', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('created_by_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.ForeignKeyConstraint(['created_by_id'], ['users.id'], ondelete='RESTRICT'),
    )
    op.create_index('ix_rules_enabled', 'rules', ['enabled'])
    op.create_index('ix_rules_priority', 'rules', ['priority'])

    # Rule executions table
    op.create_table(
        'rule_executions',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.text('gen_random_uuid()'), primary_key=True),
        sa.Column('rule_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('detection_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('matched', sa.Boolean(), nullable=False),
        sa.Column('actions_triggered', sa.JSON(), nullable=True),
        sa.Column('execution_time_ms', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['rule_id'], ['rules.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['detection_id'], ['detections.id'], ondelete='CASCADE'),
    )
    op.create_index('ix_rule_executions_rule_id', 'rule_executions', ['rule_id'])
    op.create_index('ix_rule_executions_detection_id', 'rule_executions', ['detection_id'])

    # Incidents table
    op.create_table(
        'incidents',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.text('gen_random_uuid()'), primary_key=True),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('severity', sa.Enum('CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFO', name='severity_type'), nullable=False),
        sa.Column('status', sa.Enum('NEW', 'TRIAGED', 'INVESTIGATING', 'CONTAINMENT', 'RESOLVED', 'CLOSED', name='incident_status_type'), nullable=False, server_default='NEW'),
        sa.Column('risk_score', sa.Float(), nullable=True),
        sa.Column('assigned_analyst_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.Column('resolved_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['assigned_analyst_id'], ['users.id'], ondelete='SET NULL'),
    )
    op.create_index('ix_incidents_status', 'incidents', ['status'])
    op.create_index('ix_incidents_severity', 'incidents', ['severity'])
    op.create_index('ix_incidents_created_at', 'incidents', ['created_at'])

    # Detection-Incident association
    op.create_table(
        'incident_detections',
        sa.Column('incident_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('detection_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('associated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['incident_id'], ['incidents.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['detection_id'], ['detections.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('incident_id', 'detection_id'),
    )

    # Incident timeline
    op.create_table(
        'incident_timeline',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.text('gen_random_uuid()'), primary_key=True),
        sa.Column('incident_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('old_status', sa.Enum('NEW', 'TRIAGED', 'INVESTIGATING', 'CONTAINMENT', 'RESOLVED', 'CLOSED', name='incident_status_type'), nullable=True),
        sa.Column('new_status', sa.Enum('NEW', 'TRIAGED', 'INVESTIGATING', 'CONTAINMENT', 'RESOLVED', 'CLOSED', name='incident_status_type'), nullable=False),
        sa.Column('changed_by_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('comment', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['incident_id'], ['incidents.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['changed_by_id'], ['users.id'], ondelete='RESTRICT'),
    )
    op.create_index('ix_incident_timeline_incident_id', 'incident_timeline', ['incident_id'])

    # Network devices table
    op.create_table(
        'network_devices',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.text('gen_random_uuid()'), primary_key=True),
        sa.Column('name', sa.String(255), nullable=False, unique=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('device_type', sa.Enum('FIREWALL', 'ROUTER', 'IDS', 'IDS_IPS', 'SWITCH', 'PROXY', 'SIMULATOR', name='device_type_enum'), nullable=False),
        sa.Column('vendor', sa.String(255), nullable=True),
        sa.Column('ip_address', sa.String(45), nullable=False),
        sa.Column('port', sa.Integer(), nullable=True),
        sa.Column('enabled', sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column('features', sa.JSON(), nullable=True),
        sa.Column('tags', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
    )
    op.create_index('ix_network_devices_enabled', 'network_devices', ['enabled'])
    op.create_index('ix_network_devices_device_type', 'network_devices', ['device_type'])

    # Approval requests table
    op.create_table(
        'approval_requests',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.text('gen_random_uuid()'), primary_key=True),
        sa.Column('request_type', sa.String(255), nullable=False),
        sa.Column('detection_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('incident_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('proposed_action', sa.JSON(), nullable=False),
        sa.Column('status', sa.Enum('PENDING_APPROVAL', 'APPROVED', 'REJECTED', 'EXPIRED', 'EXECUTING', 'SUCCESS', 'FAILED', name='approval_status_type'), nullable=False, server_default='PENDING_APPROVAL'),
        sa.Column('requester_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.ForeignKeyConstraint(['detection_id'], ['detections.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['incident_id'], ['incidents.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['requester_id'], ['users.id'], ondelete='RESTRICT'),
    )
    op.create_index('ix_approval_requests_status', 'approval_requests', ['status'])
    op.create_index('ix_approval_requests_created_at', 'approval_requests', ['created_at'])

    # Approval decisions table
    op.create_table(
        'approval_decisions',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.text('gen_random_uuid()'), primary_key=True),
        sa.Column('approval_request_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('approver_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('decision', sa.String(50), nullable=False),
        sa.Column('comment', sa.Text(), nullable=True),
        sa.Column('decided_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['approval_request_id'], ['approval_requests.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['approver_id'], ['users.id'], ondelete='RESTRICT'),
    )
    op.create_index('ix_approval_decisions_approval_request_id', 'approval_decisions', ['approval_request_id'])

    # Response actions table
    op.create_table(
        'response_actions',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.text('gen_random_uuid()'), primary_key=True),
        sa.Column('incident_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('approval_request_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('device_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('action_type', sa.String(255), nullable=False),
        sa.Column('target', sa.String(255), nullable=False),
        sa.Column('parameters', sa.JSON(), nullable=False),
        sa.Column('status', sa.Enum('PENDING', 'EXECUTING', 'SUCCESS', 'FAILED', 'ROLLED_BACK', name='response_status_type'), nullable=False, server_default='PENDING'),
        sa.Column('executed_by_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('result', sa.JSON(), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('executed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.ForeignKeyConstraint(['incident_id'], ['incidents.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['approval_request_id'], ['approval_requests.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['device_id'], ['network_devices.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['executed_by_id'], ['users.id'], ondelete='SET NULL'),
    )
    op.create_index('ix_response_actions_incident_id', 'response_actions', ['incident_id'])
    op.create_index('ix_response_actions_status', 'response_actions', ['status'])
    op.create_index('ix_response_actions_created_at', 'response_actions', ['created_at'])

    # Audit logs table
    op.create_table(
        'audit_logs',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.text('gen_random_uuid()'), primary_key=True),
        sa.Column('actor_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('action', sa.Enum('LOGIN', 'LOGOUT', 'CREATE', 'UPDATE', 'DELETE', 'APPROVE', 'REJECT', 'EXECUTE', 'ENRICH', 'RISK_ASSESS', name='audit_action_type'), nullable=False),
        sa.Column('resource_type', sa.String(255), nullable=False),
        sa.Column('resource_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('details', sa.JSON(), nullable=True),
        sa.Column('result', sa.String(50), nullable=False),
        sa.Column('source_ip', sa.String(45), nullable=True),
        sa.Column('user_agent', sa.String(1000), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['actor_id'], ['users.id'], ondelete='SET NULL'),
    )
    op.create_index('ix_audit_logs_actor_id', 'audit_logs', ['actor_id'])
    op.create_index('ix_audit_logs_action', 'audit_logs', ['action'])
    op.create_index('ix_audit_logs_resource_type', 'audit_logs', ['resource_type'])
    op.create_index('ix_audit_logs_created_at', 'audit_logs', ['created_at'])
    op.create_index('ix_audit_logs_result', 'audit_logs', ['result'])


def downgrade() -> None:
    """Downgrade to previous schema."""
    op.drop_index('ix_audit_logs_result')
    op.drop_index('ix_audit_logs_created_at')
    op.drop_index('ix_audit_logs_resource_type')
    op.drop_index('ix_audit_logs_action')
    op.drop_index('ix_audit_logs_actor_id')
    op.drop_table('audit_logs')
    
    op.drop_index('ix_response_actions_created_at')
    op.drop_index('ix_response_actions_status')
    op.drop_index('ix_response_actions_incident_id')
    op.drop_table('response_actions')
    
    op.drop_index('ix_approval_decisions_approval_request_id')
    op.drop_table('approval_decisions')
    
    op.drop_index('ix_approval_requests_created_at')
    op.drop_index('ix_approval_requests_status')
    op.drop_table('approval_requests')
    
    op.drop_index('ix_network_devices_device_type')
    op.drop_index('ix_network_devices_enabled')
    op.drop_table('network_devices')
    
    op.drop_index('ix_incident_timeline_incident_id')
    op.drop_table('incident_timeline')
    
    op.drop_table('incident_detections')
    
    op.drop_index('ix_incidents_created_at')
    op.drop_index('ix_incidents_severity')
    op.drop_index('ix_incidents_status')
    op.drop_table('incidents')
    
    op.drop_index('ix_rule_executions_detection_id')
    op.drop_index('ix_rule_executions_rule_id')
    op.drop_table('rule_executions')
    
    op.drop_index('ix_rules_priority')
    op.drop_index('ix_rules_enabled')
    op.drop_table('rules')
    
    op.drop_index('ix_risk_assessments_risk_score')
    op.drop_index('ix_risk_assessments_detection_id')
    op.drop_table('risk_assessments')
    
    op.drop_index('ix_enrichment_results_detection_id')
    op.drop_table('enrichment_results')
    
    op.drop_index('ix_detections_source')
    op.drop_index('ix_detections_status')
    op.drop_index('ix_detections_severity')
    op.drop_index('ix_detections_timestamp')
    op.drop_index('ix_detections_destination_ip')
    op.drop_index('ix_detections_source_ip')
    op.drop_table('detections')
    
    op.drop_table('role_permissions')
    op.drop_table('user_roles')
    op.drop_index('ix_permissions_resource_action')
    op.drop_table('permissions')
    op.drop_index('ix_roles_name')
    op.drop_table('roles')
    op.drop_index('ix_users_created_at')
    op.drop_index('ix_users_email')
    op.drop_index('ix_users_username')
    op.drop_table('users')
    
    op.execute('DROP TYPE audit_action_type')
    op.execute('DROP TYPE device_type_enum')
    op.execute('DROP TYPE response_status_type')
    op.execute('DROP TYPE approval_status_type')
    op.execute('DROP TYPE incident_status_type')
    op.execute('DROP TYPE detection_status_type')
    op.execute('DROP TYPE severity_type')
    op.execute('DROP TYPE role_type')
