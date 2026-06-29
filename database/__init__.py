from .connection import (
    get_connection,
    initialize_database
)

from .goals import (
    add_goal,
    get_goals,
    get_latest_goal,
    get_latest_goal_id,
    get_active_goal,
    get_active_goal_id,
    get_goal_history,
    get_completed_goals_count,
    get_archived_goals_count,
    get_goal_success_rate
)

from .monthly import (
    save_month,
    get_months,
    get_goal_months,
    get_active_month,
    get_active_month_by_goal
)

from .weekly import (
    save_week,
    get_weeks,
    get_active_week,
    get_active_week_by_month,
    get_current_active_week
)

from .daily import (
    save_day,
    get_days,
    get_active_day,
    get_active_day_by_week
)

from .tasks import (
    save_daily_task,
    get_daily_tasks,
    complete_daily_task,
    get_active_tasks,
    get_completed_daily_tasks,
    get_pending_daily_tasks,
    get_total_task_count,
    get_completed_task_count,
    get_pending_tasks_by_week,
    get_completed_tasks_by_week,
    delete_pending_tasks_by_week,
    save_recovery_task
)

from .progress import (
    get_daily_task_progress,
    get_month_progress,
    get_goal_progress,
    get_productivity_score
)

from .progress_engine import (
    complete_day,
    activate_next_day,
    all_tasks_completed
)

from .progress_engine import (
    get_week_progress,
    all_days_completed,
    complete_week,
    activate_next_week
)

from .progress_engine import (
    all_weeks_completed,
    complete_month,
    activate_next_month
)