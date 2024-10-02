# Generated by Django 5.1.1 on 2024-10-02 08:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("tasks", "0002_alter_task_assignee_alter_task_author"),
    ]

    operations = [
        migrations.RenameIndex(
            model_name="task",
            new_name="tasks_id_a24244_idx",
            old_name="tasks_task_id_3f110b_idx",
        ),
        migrations.RenameIndex(
            model_name="task",
            new_name="tasks_task_66d0c9_idx",
            old_name="tasks_task_task_52d46d_idx",
        ),
        migrations.RenameIndex(
            model_name="task",
            new_name="tasks_created_d28591_idx",
            old_name="tasks_task_created_5da2cb_idx",
        ),
        migrations.AlterModelTable(
            name="task",
            table="tasks",
        ),
    ]
