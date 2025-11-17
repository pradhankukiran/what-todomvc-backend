revision = "0000000006"
down_revision = "0000000005"


def upgrade(migration):
    # Tasks table
    migration.create_table(
        "task",
        """
            "entity_id" varchar(32) NOT NULL,
            "version" varchar(32) NOT NULL,
            "previous_version" varchar(32) DEFAULT '00000000000000000000000000000000',
            "active" boolean DEFAULT true,
            "changed_by_id" varchar(32) DEFAULT NULL,
            "changed_on" timestamp NULL DEFAULT CURRENT_TIMESTAMP,
            "title" varchar(255) NOT NULL,
            "completed" boolean DEFAULT false,
            "person_id" varchar(32) NOT NULL,
            PRIMARY KEY ("entity_id")
        """
    )
    migration.add_index("task", "task_person_id_ind", "person_id")
    migration.add_index("task", "task_completed_ind", "completed")
    migration.add_index("task", "task_person_completed_ind", "person_id, completed")

    # Audit table
    migration.create_table(
        "task_audit",
        """
            "entity_id" varchar(32) NOT NULL,
            "version" varchar(32) NOT NULL,
            "previous_version" varchar(32) DEFAULT '00000000000000000000000000000000',
            "active" boolean DEFAULT true,
            "changed_by_id" varchar(32) DEFAULT NULL,
            "changed_on" timestamp NULL DEFAULT CURRENT_TIMESTAMP,
            "title" varchar(255) NOT NULL,
            "completed" boolean DEFAULT false,
            "person_id" varchar(32) NOT NULL,
            PRIMARY KEY ("entity_id", "version")
        """
    )

    migration.update_version_table(version=revision)


def downgrade(migration):
    migration.drop_table(table_name="task")
    migration.drop_table(table_name="task_audit")
    migration.update_version_table(version=down_revision)
